#
# This module handles extended AI kit selection and dynamic spawning
# NOTE: Used and redistributed with permission from [VG]X0R
#
# Coders:
# Original Author: [VG]X0R
# Coder: [R-DEV]papadanku
#

# Import Python modules
import math
import os
import random
import re
import zipfile

# Import bf2 modules
import bf2
import host

# Import Reality modules
import realitykits as rkits
import realityserver as rserver
import realitytimer as rtimer

# Import Reality configs
from realityconfig_coop import C


g_ai_kitSlots = {}
g_spawnTime = {}


def init():
    if rserver.isCoopServer():
        if C["RANDOMIZE_KITS"] == 1:
            host.registerHandler("PlayerSpawn", onPlayerSpawn)
            host.registerGameStatusHandler(onGameStatusChanged)
        if (C["SPAWN_TIME_MODIFIER"] >= 1) and (C["BOT_DYNAMIC_RESPAWN"] == 1):
            host.registerHandler("PlayerKilled", onPlayerKilled)
            host.registerHandler("PlayerDeath", onPlayerDeath)


class aiKitSlot(object):
    """
    Setup an AI team's kitSlot attributes
    """

    # NOTE: KIT_TYPES needs to be in this order to comply with vbf2's spawn-order
    KIT_TYPES = ("specops", "sniper", "assault", "support", "engineer", "medic", "at")

    def __init__(self, team):
        # Initialize kitSlot's team information
        self.faction = bf2.gameLogic.getTeamName(team).lower()
        self.variant = self.faction + rkits.getKitTeamVariants(team)

        # Initialize kitSlot's attributes
        self.kits = dict.fromkeys(self.KIT_TYPES)
        for key in self.kits.keys():
            self.kits.update({key: set()})

    def isValidKit(self, kit):
        for excludedKit in C["EXCLUDED_KITS"]:
            if excludedKit in kit:
                return False
        return True

    # Get all variant kit filepaths
    def getKitFilePaths(self, variantFile):
        # Read content from file
        fileText = str(variantFile.read().decode().strip())

        # Find kits based on variant
        if "v_arg1" not in fileText:
            kitPattern = re.compile("(.*)", re.DOTALL)
        elif self.variant == self.faction:
            kitPattern = re.compile('(?<="else")(.*?)(?=endIf)', re.DOTALL)
        else:
            kitPattern = re.compile('(?<="%s")(.*?)(?=elseIf|else|endIf)' % (self.variant), re.DOTALL)

        kitBlock = re.search(kitPattern, fileText).group()
        kits = re.findall(re.compile("(\S+\.tweak)"), kitBlock)
        return kits

    # Generate singleplayer kit list based on the archive
    def getKitData(self):
        # Archive data
        archivePath = os.path.join(host.sgl_getModDirectory(), "content", "objects_common_server.zip")
        archiveFile = zipfile.ZipFile(archivePath, "r")

        # Variant data
        variantPath = "/".join(["kits", self.faction, "variants.inc"])
        variantFile = archiveFile.open(variantPath, "r")

        # Get paths to kit files
        try:
            kitSum = set()
            for path in self.getKitFilePaths(variantFile):
                kitPath = "/".join(["kits", self.faction, path])
                kitFile = archiveFile.open(kitPath, "r")
                kitText = str(kitFile.read().decode())
                try:
                    kitName = re.search("(?<=ObjectTemplate\.create Kit )(\w+)", kitText).group()
                    kitType = re.search("(?<=ObjectTemplate\.kitType )(\w+)", kitText).group().lower()
                    if rkits.kitExists(kitName) and self.isValidKit(kitName):
                        kitSum.add(kitName)
                        self.kits[kitType].add(kitName)
                    kitFile.close()
                except:
                    kitFile.close()
                    continue

            # Process kit choices into tuples, add as object attributes
            # NOTE: Empty kitSlots get random kits
            for key, value in self.kits.items():
                if value:
                    self.kits.update({key: tuple(value)})
                else:
                    self.kits.update({key: tuple(kitSum)})
        finally:
            archiveFile.close()
            variantFile.close()
        return


def onGameStatusChanged(status):
    """
    Cache kit choices and weights for each team
    """

    global g_ai_kitSlots
    global g_spawnTime

    # Get each team's kitSlot data
    if status == bf2.GameStatus.Playing:
        g_ai_kitSlots.clear()
        g_spawnTime.clear()
        for team in [1, 2]:
            g_ai_kitSlots[team] = aiKitSlot(team)
            g_ai_kitSlots[team].getKitData()
    return


def onPlayerSpawn(player, soldier):
    """
    Modify AI's kit choices
    """
    if player.isAIPlayer():
        team = player.getTeam()
        for index, kitType in enumerate(g_ai_kitSlots[team].KIT_TYPES):
            kit = random.choice(g_ai_kitSlots[team].kits[kitType])
            soldier = rkits.g_kits_slots[team][index].Soldier
            host.rcon_invoke("gameLogic.setKit %s %s %s %s" % (team, index, kit, soldier))
    else:
        pass
    return


class aiSpawner(object):
    """
    Modify spawn time depending on team ratio
    """

    global g_spawnTime

    @staticmethod
    def fastRespawn(victimName):
        g_spawnTime.update({victimName: 0})
        return

    @staticmethod
    def dynamicRespawn(victimName):
        # teamOne = AI; teamTwo = Human
        teamOneCount = bf2.playerManager.getNumberOfPlayersInTeam(1)
        teamTwoCount = bf2.playerManager.getNumberOfPlayersInTeam(2)

        # Round to nearest 10th; minimum player count of 5
        teamTwoCount = max(round(teamTwoCount, -1), 5)
        # Make minimum possible respawn time 30 seconds
        countRatio = teamOneCount / teamTwoCount
        spawnTime = min(30, math.ceil(countRatio * C["SPAWN_TIME_MODIFIER"]))

        # Cache results
        g_spawnTime.update({victimName: spawnTime})
        return


def onPlayerKilled(victim, attacker, weaponObject, assists, victimSoldierObject):
    """
    Modify spawn times based on certain conditions
    NOTE: Using setDamage on nextTick seems to also cause crashes, albeit less frequently
    NOTE: Instead, do so 1sec after event
    """

    try:
        if victim.isValid() and victim.isAIPlayer():
            victimName = victim.getName()
            if not attacker:
                rtimer.fireOnce(aiSpawner.fastRespawn, 1, victimName)
            elif (attacker == victim) or (attacker.getTeam() == victim.getTeam()):
                rtimer.fireOnce(aiSpawner.fastRespawn, 1, victimName)
            elif attacker.getTeam() != victim.getTeam():  # PlayerEnemyKilled
                rtimer.fireOnce(aiSpawner.dynamicRespawn, 1, victimName)
    except:
        pass
    return


def onPlayerDeath(victim, soldier):
    """
    Dead bot: Respawn time is dynamic respawn time
    """

    global g_spawnTime

    try:
        if victim.isAIPlayer():
            victim.setTimeToSpawn(g_spawnTime[victim.getName()])
    except:
        pass
    return
