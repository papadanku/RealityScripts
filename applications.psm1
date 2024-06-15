
class Application {
    static [int] GetOptionIndex([string[]] $options, [string] $initialPrompt) {
        Write-Host $initialPrompt
        for ($i = 0; $i -lt $options.Count; $i++) {
            Write-Host "`t$($i + 1). $($options[$i])"
        }

        # Allow the user to choose between N options
        [int]$choice = -1
        do {
            $response = Read-Host -Prompt "Enter your choice"
            $choice = [int]::Parse($response)
        } while ($choice -lt 0 || $choice -gt $options.Length)

        return $choice;
    }
}