
Read-Host "Enter Repo Path" | Set-Location

$SearchPath = Join-Path @(Get-Location) -ChildPath "objects" -AdditionalChildPath "kits"
$VariantFilePaths = [System.IO.Directory]::GetFiles($searchPath, "variants.inc", "AllDirectories")
$MissingKits = @{}

function Search-MissingTemplates() {       
    foreach ($path in $VariantFilePaths) {
        $factionDirectory = [System.IO.Path]::GetDirectoryName($path)
        $variantFileText = Get-Content $path
        $variants = [regex]::Matches($variantFileText, '(?s)("\w+"|else\b)(.*?)(?=else|$)')

        foreach ($variant in $variants) {
            Search-Kits -FactionPath $factionDirectory -VariantMatch $variant
        }
    }
}

function Search-Kits() {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [string]$FactionPath,
        [System.Text.RegularExpressions.Match]$VariantMatch
    )

    # Convert match groups to strings
    $faction = [System.IO.Path]::GetFileName($FactionPath)
    $variant = $VariantMatch.Groups[1].ToString()
    $variant = (($variant -eq "else") ? $faction : $variant).Trim('"')
    $kitFiles = $VariantMatch.Groups[2].ToString()

    Write-Host "Checking $variant..."

    # Initialize kit collections
    $loadedKits = New-Object -TypeName System.Collections.Generic.HashSet[string]
    $allocatedKits = New-Object -TypeName System.Collections.Generic.HashSet[string]

    # Allocate kire from the variant runs and preloaded
    $kits = [regex]::Matches($kitFiles, '(?<=run )[\w\/]+\.tweak')

    foreach ($kit in $kits) {
        $kitTweakFilePath = Join-Path -Path $FactionPath -ChildPath $kit.Value
        $kitTweakFileText = Get-Content $kitTweakFilePath

        try {
            if ($kitTweakFilePath.Contains("preload")) {
                $kitMatches = [regex]::Matches($kitTweakFileText, '(?<=ObjectTemplate\.setObjectTemplate \d )\w+')
                foreach ($kitMatch in $kitMatches) {
                    [void]$allocatedKits.Add($kitMatch.Value)
                }
            }
            else {
                $kitMatches = [regex]::Matches($kitTweakFileText, '(?<=ObjectTemplate\.create Kit )\w+')
                foreach ($kitMatch in $kitMatches) {
                    [void]$loadedKits.Add($kitMatch)
                }
            }
        }
        catch {
            continue
        }
    }

    $loadedKits.ExceptWith($allocatedKits)
    if ($loadedKits.Count -gt 0) {
        [void]$MissingKits.Add($variant, $loadedKits)
    }
}

# Main app
Search-MissingTemplates
$MissingKits | Format-List -AutoSize
