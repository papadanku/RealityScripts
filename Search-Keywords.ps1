
#. .\Initialize-Script.ps1

Set-Location "D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo"

$keywordSets = @{}

# Get all code files recursively
Write-Host "Getting code files..."
$pattern = [regex]('\w+(?:\.\w+)+')

# Search all files in direactory for keywords
$Files = Get-ChildItem -Recurse -Path @(Get-Location) | Where-Object { $_.Extension -match '\.(con|tweak|inc)$' }

foreach ($file in $Files) {
    $fileText = Get-Content -Path $file.FullName
    $vars = $pattern.Matches($fileText)

    if ($vars)
    {
        foreach ($var in $vars) {
            $varComponents = $var -split '\.'
            for ($i = 0; $i -lt $varComponents.Count; $i++) {
                $id = $i.ToString()
                if (-not $keywordSets.ContainsKey($id)) {
                    $keywordSets[$id] = [System.Collections.Generic.HashSet[string]]::new()
                }
                [void]$keywordSets[$id].Add($varComponents[$i])
            }
        }
    }
}

# Print the resulting dictionary
$keywordSets | Out-File -FilePath "output.txt"
