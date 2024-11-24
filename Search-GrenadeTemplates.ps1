
. .\Initialize-Script.ps1

$WeaponFiles = Get-ChildItem -Recurse -Filter "*.tweak" -Path @($GlobalPath)

$totalGrenadeFiles = 0
$totalAIFiles = 0

foreach ($weaponFilePath in $WeaponFiles) {
    $FileContent = Get-Content -Path $weaponFilePath.FullName
    $IsGrenade = $FileContent -match 'smokegrenade\.tga'
    $HasAITemplate = $FileContent -match 'aiTemplate hgr_smoke_AI'

    if ($IsGrenade -and $HasAITemplate) {
        $totalAIFiles += 1
    } elseif ($IsGrenade) {
        $totalGrenadeFiles += 1
        Write-Host $weaponFilePath.FullName
    }
}

Write-Host "Number of grenades: $totalGrenadeFiles"
Write-Host "Number of grenades with AI: $totalAIFiles"
