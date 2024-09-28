
$levelsDir = "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo\levels"
$levelFilePaths = Get-ChildItem -Path $levelsDir -Depth 1 -Filter "*.con" | Where-Object { $_.Name -match "(sky|water)" }

foreach ($path in $levelFilePaths) {
    $fileText = Get-Content $path
    $colorSettings = $fileText -match "[\w\.]*?color\s+[\d\.\/]+"

    foreach ($oldSetting in $colorSettings) {
        $oldSetting -match "([\w\.]*?color)\s+([\d\.\/]+)"

        $tempSettingName = $Matches[1]
        $settingValueGroup = $Matches[2] -split '/' | ForEach-Object {
            if ($Matches[1].ToLower().Contains("fogcolor")) {
                $toFloat = [float]$_ / 256.0
                $toFloat *= $toFloat
                $toFloat * 256.0
            }
            else {
                if ($path.BaseName.ToLower().Contains("water")) {
                    [float]$_ * [float]$_
                }
                else {
                    [System.Math]::Sqrt([float]$_)
                }
            }
        }

        $settingValueGroup = $settingValueGroup -join "/"
        $newSetting = "$tempSettingName $settingValueGroup"

        $fileText = $fileText -replace $oldSetting, $newSetting
    }

    Set-Content $path -Value $fileText
}
