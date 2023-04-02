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
g_spawnTime_cache = {}


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

    def __init__(self, team):
        # Initialize kitSlot's team information
        self.team = team
        self.teamName = bf2.gameLogic.getTeamName(self.team).lower()
        self.variant = self.teamName + rkits.getKitTeamVariants(self.team)

        # Initialize kitSlot's attributes
        # NOTE: self.kitTypes needs to be in this order to comply with vbf2's spawn-order
        self.kitTypes = ("specops", "sniper", "assault", "support", "engineer", "medic", "at")
        self.kits = dict.fromkeys(self.kitTypes)

    def isValidKit(self, kit):
        for excludedKit in C["EXCLUDED_KITS"]:
            if excludedKit in kit:
                return False
        return True

    # Get all variant kit filepaths
    def getKitFilePaths(self, variantFile):
        kitPaths = []
        variantFound = False

        # NOTE: This is a hack. All factions have >1 variants, so default's last
        if self.variant == self.teamName:
            variantLine = "else"
        else:
            variantLine = 'v_arg1 == "{}"'.format(self.variant)

        for line in variantFile:
            if variantLine in line:
                variantFound = True
                continue
            if variantFound:
                if "run" not in line:
                    break
                elif "preload" not in line:
                    line = str(line.decode().strip())
                    path = "/".join(["kits", self.teamName, line.split()[-1]])
                    kitPaths.append(path)

        return kitPaths

    # Generate singleplayer kit list based on the archive
    def getKitData(self):
        # Archive data
        archivePath = os.path.join(host.sgl_getModDirectory(), "content", "objects_common_server.zip")
        archiveFile = zipfile.ZipFile(archivePath, "r")

        # Variant data
        variantPath = "/".join(["kits", self.teamName, "variants.inc"])
        variantFile = archiveFile.open(variantPath, "r")

        try:
            # Initialize kit data
            kitSet = set()
            kitDict = dict.fromkeys(self.kitTypes)
            for key in kitDict.keys():
                kitDict.update({key: set()})

            # Get paths to kit files
            for path in self.getKitFilePaths(variantFile):
                kitFile = archiveFile.open(path, "r")
                try:
                    kitName = ""
                    kitType = ""
                    for kitLine in kitFile:
                        kitLine = str(kitLine.decode().strip())
                        if "ObjectTemplate.create Kit" in kitLine:
                            kitName = kitLine.split(" ")[-1]
                        if "ObjectTemplate.kitType" in kitLine:
                            kitType = kitLine.split(" ")[-1].lower()
                        if (kitName and kitType) and rkits.kitExists(kitName):
                            if self.isValidKit(kitName):
                                kitSet.add(kitName)
                                kitDict[kitType].add(kitName)
                            break
                finally:
                    kitFile.close()

            # Process kit choices into tuples, add as object attributes
            # NOTE: Empty kitSlots get random kits
            for key, value in kitDict.items():
                if value:
                    self.kits.update({key: tuple(value)})
                else:
                    self.kits.update({key: tuple(kitSet)})
        finally:
            archiveFile.close()
            variantFile.close()


def onGameStatusChanged(status):
    """
    Cache kit choices and weights for each team
    """

    global g_ai_kitSlots
    global g_spawnTime_cache

    if status == bf2.GameStatus.Playing:
        g_ai_kitSlots.clear()
        g_spawnTime_cache.clear()

        # Get each team's kitSlot data
        for team in [1, 2]:
            g_ai_kitSlots[team] = aiKitSlot(team)
            g_ai_kitSlots[team].getKitData()


def onPlayerSpawn(player, soldier):
    """
    Modify AI's kit choices
    """
    if not player.isAIPlayer():
        return

    # Fill the spawner's kitSlots with a random kit
    team = player.getTeam()
    for kitIndex, kitType in enumerate(g_ai_kitSlots[team].kitTypes):
        kit = random.choice(g_ai_kitSlots[team].kits[kitType])
        soldier = rkits.g_kits_slots[team][kitIndex].Soldier
        host.rcon_invoke("gameLogic.setKit %s %s %s %s" % (team, kitIndex, kit, soldier))


class aiSpawner(object):
    """
    Modify spawn time depending on team ratio
    """

    global g_spawnTime_cache

    @staticmethod
    def fastRespawn(victim):
        soldier = victim.getDefaultVehicle()
        if soldier:
            soldier.setDamage(0)
            victim.setTimeToSpawn(0)

    @staticmethod
    def dynamicRespawn(victim):
        # Clear cache if it is larger than a certain size
        if len(g_spawnTime_cache) > 256:
            g_spawnTime_cache.clear()

        # teamOne = AI; teamTwo = Human
        teamOneCount = bf2.playerManager.getNumberOfPlayersInTeam(1)
        teamTwoCount = bf2.playerManager.getNumberOfPlayersInTeam(2)
        functionArgs = str(teamOneCount + teamTwoCount)

        if functionArgs in g_spawnTime_cache:
            spawnTime = g_spawnTime_cache[functionArgs]
        else:
            # Round to nearest 10th; minimum player count of 5
            teamTwoCount = max(round(teamTwoCount, -1), 5)
            # Make minimum possible respawn time 30 seconds
            countRatio = teamOneCount / teamTwoCount
            spawnTime = min(30, math.ceil(countRatio * C["SPAWN_TIME_MODIFIER"]))
            # Cache results
            g_spawnTime_cache[functionArgs] = spawnTime

        victim.setTimeToSpawn(spawnTime)

def onPlayerKilled(victim, attacker, weaponObject, assists, victimSoldierObject):
    """
    Modify spawn times based on certain conditions
    NOTE: Using setDamage on nextTick seems to also cause crashes, albeit less frequently
    NOTE: Instead, do so 1sec after event
    TODO: Fix refire when fastSpawn() happens (fastSpawn -> dynamicSpawn)
    """

    try:
        playerEvents = {
            # Do not set spawn time if: The victim is non-AI, invalid attacker/victim
            "invalid": [
                not victim.isAIPlayer(),
                not victim,
                not victim.isValid(),
                victim is None,
                attacker is None,
                victim.isValid() is False,
                attacker.isValid() is False,
            ],
            # Set fast spawn-time for: victimless death, suicide, or teamkill
            "fast": [
                not attacker,
                attacker is victim,
                attacker.getTeam() == victim.getTeam(),
            ],
        }

        if any(playerEvents["invalid"]):
            return
        elif any(playerEvents["fast"]):
            rtimer.fireOnce(aiSpawner.fastRespawn, 1, victim)
        else: # PlayerEnemyKilled
            rtimer.fireOnce(aiSpawner.dynamicRespawn, 1, victim)
    except:
        pass


def onPlayerDeath(victim, soldier):
    """
    Dead bot: Respawn time is dynamic respawn time
    """

    try:
        if victim is None:
            return
        else:
            if victim.isAIPlayer():
                rtimer.fireOnce(aiSpawner.dynamicRespawn, 1, victim)
    except:
        pass
