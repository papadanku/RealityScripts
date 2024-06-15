
Read-Host "Enter Repo Path" -ErrorAction Stop | Set-Location

# Get all audio files recursively
Write-Host "Getting audio files..."
$audioFiles = Get-ChildItem -Recurse -Path @(Get-Location) | Where-Object { $_.Extension -match '\.(wav|ogg)$' }

# Get file hashes for all audio files
Write-Host "Getting file hashes..."
$fileHashes = $audioFiles | Get-FileHash

# Group files by hash and identify duplicates (more than one file per hash)
Write-Host "Finding duplicate files"
$duplicateGroups = $fileHashes | Group-Object -Property Hash | Where-Object { $_.Count -gt 1 }

# Sort duplicate files based on Path and Hash
$duplicateGroups = $duplicateGroups | ForEach-Object { $_.Group | Select-Object Path, Hash }

# Output duplicate files to a sheet file
$outputPath
while (-not @(Test-Path $outputPath)) {
    $outputPath = Read-Host "Enter output file path"
}

$duplicateGroups | Export-Csv -Path "$outputPath.csv" -Encoding UTF8
