
. .\Initialize-Script.ps1

# Get all audio files recursively
Write-Host "Getting audio files..."
$AudioFiles = Get-ChildItem -Recurse -Path @(Get-Location) | Where-Object { $_.Extension -match '\.(wav|ogg)$' }

# Get file hashes for all audio files
Write-Host "Getting file hashes..."
$FileHashes = $AudioFiles | Get-FileHash

# Group files by hash and identify duplicates (more than one file per hash)
Write-Host "Finding duplicate files"
$DuplicateGroups = $FileHashes | Group-Object -Property Hash | Where-Object { $_.Count -gt 1 }

# Sort duplicate files based on Path and Hash
$DuplicateGroups = $DuplicateGroups | ForEach-Object { $_.Group | Select-Object Path, Hash }

# Output duplicate files to a sheet file
$OutputDirectory = Read-Host "Enter output file path"
while (-not @(Test-Path $OutputDirectory -PathType Directory)) {
    $OutputDirectory = Read-Host "Incorrect directory. Enter output directory"
}

$OutputFile = Read-Host "Enter file name"

$DuplicateGroups | Export-Csv -Path "$OutputFile.csv" -Encoding UTF8
