
$levelsDir = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\levels"
$levelFilePaths = Get-ChildItem -Path $levelsDir -Depth 1 -Filter "*.con" | Where-Object { $_.Name -match "(sky|water)" }

foreach ($path in $levelFilePaths) {
    $fileText = Get-Content $path
    $colorSettings = $fileText -match "[\w\.]*?color\s+[\d\.\/]+"

    foreach ($oldSetting in $colorSettings) {
        $oldSetting -match "([\w\.]*?color)\s+([\d\.\/]+)"

        $tempSettingName = $Matches[1]
        $tempSettingNameLower = $tempSettingName.ToLower()
        $settingValueGroup = $Matches[2] -split '/' | ForEach-Object {
            if ($tempSettingNameLower.Contains("fogcolor")) {
                $toFloat = [float]$_ / 256.0
                $toFloat *= $toFloat
                $toFloat * 256.0
            }
            elseif ($path.BaseName.ToLower().Contains("water") -and $tempSettingNameLower.Contains("watercolor")) {
                [float]$_ * [float]$_
            }
            else {
                [float]$_
            }
        }

        $settingValueGroup = $settingValueGroup -join "/"
        $newSetting = "$tempSettingName $settingValueGroup"

        $fileText = $fileText -replace $oldSetting, $newSetting
    }

    Set-Content $path -Value $fileText
}
