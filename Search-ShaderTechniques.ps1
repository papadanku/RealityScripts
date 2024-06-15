
Read-Host "Enter repo path" | Set-Location

$SearchPath = Join-Path -Path @(Get-Location) -ChildPath "shaders"
$VariantFilePaths = Get-ChildItem -Recurse -Path $SearchPath -Filter "*.fx*"
$TechniqueTable = @{}

function Search-ShaderTechniques {
    Write-Host "Searching shader techniques..."

    $pattern = [regex]('(?<=technique )\w+')
    foreach ($path in $VariantFilePaths) {
        $fileText = Get-Content $path
        $techniques = $pattern.Matches($fileText)

        if ($techniques.Count -gt 0) {
            $techniqueSet = New-Object System.Collections.Generic.HashSet[string]
            foreach ($technique in $techniques) {
                [void]$techniqueSet.Add($technique)
            }
            $TechniqueTable[$path] = $techniqueSet
        }
    }
}

# Main program
Search-ShaderTechniques
$TechniqueTable | Format-List
