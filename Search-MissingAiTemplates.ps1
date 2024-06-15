
Read-Host "Enter Repo Path" | Set-Location
$FilePaths = @{}
$FilePaths[".ai"] = New-Object System.Collections.Generic.HashSet[string]
$FilePaths[".tweak"] = New-Object System.Collections.Generic.HashSet[string]
$AITemplates = New-Object System.Collections.Generic.HashSet[string]
$MissingTemplates = @{}

function Get-Directories {
    $searchDictionaries = @()
    
    $menuOptions = @("Vehicles", "Weapons", "Objects", "Kits")
    $appChoice = [Application]::GetOptionIndex($menuOptions, "Check AI Templates for:")
    switch ($appChoice) {
        1 { $searchDictionaries = ("vehicles") }
        2 { $searchDictionaries = ("weapons") }
        3 { $searchDictionaries = ("staticobjects", "dynamicobjects") }
        4 { $searchDictionaries = ("kits") }
    }

    # Initialize file paths
    $allFilePaths = New-Object System.Collections.Generic.HashSet[string]

    # Get files from selected directories
    foreach ($directory in $searchDictionaries) {
        $searchPath = Join-Path -Path @(Get-Location) -ChildPath "objects" -AdditionalChildPath $directory
        $allFilePaths.UnionWith([System.IO.Directory]::GetFiles($searchPath, "*", "AllDirectories"))
    }

    # Group filepaths by extension
    foreach ($filePath in $allFilePaths) {
        $fileExtension = [System.IO.Path]::GetExtension($filePath);
        if ($FilePaths.ContainsKey($fileExtension)) {
            $FilePaths[$fileExtension].Add($filePath)
        }
    }
}

function Get-Templates {
    # Let the user know that the app is working
    Write-Host "Gathering AI templates..."

    foreach ($path in $FilePaths[".ai"]) {
        $fileText = Get-Content $path
        $templates = [regex]::Matches($fileText, '(?:(?:ai|kit|weapon)Template(?:Plugin)?\.create )(\w+)')

        foreach ($template in $templates) {
            $AITemplates.Add($template.Groups[1].ToString())
        }
    }
}

function Find-Templates {
    # Let the user know that the app is working
    Write-Host "Checking AI templates..."

    # Accumulate missing templates
    foreach ($path in $FilePaths[".tweak"]) {
        $fileText = Get-Content $path
        $templates = [regex]::Matches($fileText, '(?:\w+\.aiTemplate )(\w+)')

        foreach ($template in $templates) {
            $aiTemplate = $template.Groups[1].ToString()
            if (-not $AITemplates.Contains($aiTemplate)) {
                $key = Resolve-Path $path -Relative
                $MissingTemplates.Add($key, $aiTemplate)
            }
        }
    }
}

# Main main program
Get-Directories
Get-Templates
Find-Templates
$MissingTemplates | Format-List -AutoSize
