
. .\Initialize-Script.ps1

$keywordSets = [System.Collections.Generic.HashSet[string]]::new()

# Get all code files recursively
Write-Host "Parsing files..."
$pattern = [regex]('ObjectTemplate.physicsType\s+(\w+)')

# Search all files in direactory for keywords
$Files = Get-ChildItem -Recurse -Path @($GlobalPath) | Where-Object { $_.Extension -match '\.(ai)$' }

foreach ($file in $Files) {
    $fileText = Get-Content -Path $file.FullName
    $vars = $pattern.Matches($fileText)

    foreach ($var in $vars) {
        [void]$keywordSets.Add($var.Groups[1].Value)
    }
}

# Print the resulting set
$keywordSets
