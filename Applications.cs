
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

abstract class Application(string path)
{
    public string RepoPath = path;
    public abstract void Execute();

    static public int GetChoiceIndex(Dictionary<int, string> options, string initialPrompt)
    {
        StringBuilder prompt = new();
        prompt.AppendLine(initialPrompt);

        foreach (KeyValuePair<int, string> option in options)
        {
            prompt.AppendLine($"[{option.Key}] {option.Value}");
        }
        Console.WriteLine(prompt);

        // Allow the user to choose between N options
        int choice;
        do
        {
            Console.Write("Enter your choice: ");
            string? response = Console.ReadLine();
            choice = int.Parse(response);
        } while (!options.ContainsKey(choice));

        return choice;
    }
}

/// <summary>
/// Application for processing AI templates
/// </summary>
class AI(string path) : Application(path)
{
    private readonly List<string> _searchDirectories = [];
    private readonly List<string> _aiFilePaths = [];
    private readonly List<string> _tweakFilePaths = [];
    private readonly HashSet<string> _aiTemplates = [];

    public override void Execute()
    {
        Console.WriteLine("\nStarting application...\n");
        GetDirectories();
        GetTemplates();
        CheckTemplates();
    }

    private void GetDirectories()
    {
        // Build available options
        Dictionary<int, string> options = new()
        {
            { 1, "Vehicles" },
            { 2, "Weapons" },
            { 3, "Objects" },
            { 4, "Kits" }
        };

        int appChoice = GetChoiceIndex(options, "\nCheck AI Templates for:");
        switch (appChoice)
        {
            case 1:
                _searchDirectories.Add("vehicles");
                break;
            case 2:
                _searchDirectories.Add("weapons");
                break;
            case 3:
                _searchDirectories.Add("staticobjects");
                _searchDirectories.Add("dynamicobjects");
                break;
            case 4:
                _searchDirectories.Add("kits");
                break;
        }

        // Construct directories to search
        foreach (string directory in _searchDirectories)
        {
            string searchPath = Path.Combine(RepoPath, "objects", directory);
            _aiFilePaths.AddRange(Directory.GetFiles(searchPath, "*.ai", SearchOption.AllDirectories));
            _tweakFilePaths.AddRange(Directory.GetFiles(searchPath, "*.tweak", SearchOption.AllDirectories));
        }
    }

    public void GetTemplates()
    {
        // Let the user know that the app is working
        Console.WriteLine("Gathering AI templates...");

        foreach (string path in _aiFilePaths)
        {
            string fileText = File.ReadAllText(path);
            MatchCollection templates = Regex.Matches(fileText, @"(?:(?:ai|kit|weapon)Template(?:Plugin)?\.create )(\w+)", RegexOptions.Compiled);

            foreach (Match template in templates)
            {
                string aiTemplate = template.Groups[1].ToString();
                _aiTemplates.Add(aiTemplate);
            }
        }
    }

    public void CheckTemplates()
    {
        // Let the user know that the app is working
        Console.WriteLine("Checking AI templates...");

        foreach (string path in _tweakFilePaths)
        {
            string fileText = File.ReadAllText(path);
            MatchCollection templates = Regex.Matches(fileText, @"(?<=\.aiTemplate )\w+", RegexOptions.Compiled);

            foreach (Match template in templates)
            {
                string aiTemplate = template.Value;
                if (!_aiTemplates.Contains(aiTemplate))
                {
                    Console.WriteLine($"\n{template} has missing template!\n\t{path}");
                }
            }
        }
    }
}

/// <summary>
/// Application for processing kit templates
/// </summary>
class Kits : Application
{
    private readonly string[] _variantFilePaths = [];

    public Kits(string path) : base(path)
    {
        string searchPath = Path.Combine(RepoPath, "objects", "kits");
        _variantFilePaths = Directory.GetFiles(searchPath, "variants.inc", SearchOption.AllDirectories);
    }

    public override void Execute()
    {
        Console.WriteLine("\nStarting application...\n");

        string factionDirectory;
        string variantFileText;

        foreach (string path in _variantFilePaths)
        {
            factionDirectory = Path.GetDirectoryName(path);
            variantFileText = File.ReadAllText(path);

            MatchCollection variants = Regex.Matches(variantFileText, @"(""\w+""|else\b)(.*?)(?=else|$)", RegexOptions.Singleline);
            foreach (Match variant in variants)
            {
                CheckTemplates(factionDirectory, variant);
            }
        }
    }

    private static void CheckTemplates(string factionDirectory, Match match)
    {
        // Convert match groups to strings
        string faction = Path.GetFileName(factionDirectory);
        string variant = match.Groups[1].ToString();
        variant = (variant == "else") ? $@"""{faction}""" : variant;
        string kitFiles = match.Groups[2].ToString();

        // Initialize kit collections
        HashSet<string> loadedKits = [];
        HashSet<string> allocatedKits = [];

        // Allocate kits from the variant runs and preloaded
        MatchCollection kits = Regex.Matches(kitFiles, @"(?<=run )[\w\/]+\.tweak");
        foreach (Match kit in kits)
        {
            string kitTweakFilePath = Path.Combine(factionDirectory, kit.Value);
            string kitTweakFileText = File.ReadAllText(kitTweakFilePath);
            MatchCollection matches;

            if (kitTweakFilePath.Contains("preload"))
            {
                matches = Regex.Matches(kitTweakFileText, @"(?<=ObjectTemplate\.setObjectTemplate \d )\w+");
                allocatedKits.UnionWith(matches.Select(match => match.Value).ToHashSet());
            }
            else
            {
                matches = Regex.Matches(kitTweakFileText, @"(?<=ObjectTemplate\.create Kit )\w+");
                loadedKits.UnionWith(matches.Select(match => match.Value).ToHashSet());
            }
        }

        // Compare the loaded and allocated kits
        IEnumerable<string> missingKits = loadedKits.Except(allocatedKits);
        if (missingKits.Any())
        {
            Console.WriteLine($"{variant}:\n\t{string.Join($"\n\t", missingKits)}");
        }
        else
        {
            Console.WriteLine($"{variant}: No missing kits");
        }
    }
}

/// <summary>
/// Application for processing shader files
/// </summary>
class Shaders : Application
{
    private readonly string[] _variantFilePaths;

    public Shaders(string path) : base(path)
    {
        string searchPath = Path.Combine(RepoPath, "shaders");
        _variantFilePaths = Directory.GetFiles(searchPath, "*.fx*", SearchOption.AllDirectories);
    }

    public override void Execute()
    {
        Console.WriteLine("\nStarting application...\n");

        string pattern = @"(?<=technique )\w+";
        foreach (string path in _variantFilePaths)
        {
            string fileText = File.ReadAllText(path);
            MatchCollection techniques = Regex.Matches(fileText, pattern);

            // Display shader files and their respective techniques
            if (techniques.Count != 0)
            {
                Console.WriteLine(path);
                foreach (Match technique in techniques)
                {
                    Console.WriteLine($"\t{technique.Value}");
                }
            }
        }
    }
}

class FileManager(string path) : Application(path)
{
    public override void Execute()
    {
        Console.WriteLine("\nStarting application...\n");

        Console.Write("Enter output file directory: ");
        string fileDirectory = Console.ReadLine();

        Console.Write("Enter output file name: ");
        string fileName = Console.ReadLine();

        string outputFilePath = Path.Combine(fileDirectory, $"{fileName}.txt");

        Dictionary<int, HashSet<string>> fileExtensions = new()
        {
            { 1, [".ogg", ".wav"] },
            { 2, [".con", ".tweak"] }
        };

        // Create menu options
        Dictionary<int, string> menuOptions = new()
        {
            { 1, "Audio Files" },
            { 2, "Configuration Files" }
        };

        int appChoice = GetChoiceIndex(menuOptions, "Check Duplicate Files for:");
        FindDuplicateFiles(RepoPath, fileExtensions[appChoice], outputFilePath);
    }

    static private string GetFileHash(string filePath)
    {
        // Initialize SHA256 filestream
        using FileStream fileStream = File.OpenRead(filePath);
        StringBuilder stringBuilder = new();

        // Compute the fileStream's hash value
        byte[] fileHash = SHA256.HashData(fileStream);

        // Convert the fileStream's hash value to a string
        return BitConverter.ToString(fileHash).Replace("-", "");
    }

    public static void FindDuplicateFiles(string directoryPath, HashSet<string> extensions, string outputFilePath)
    {
        // This dictionary stores hashes and audio file paths associated with the hash
        Dictionary<string, List<string>> fileMap = [];

        // Use Directory.EnumerateFiles to efficiently retrieve and filter files
        Console.WriteLine("Gathering files...");
        IEnumerable<string> files = Directory.EnumerateFiles(directoryPath, "*", SearchOption.AllDirectories)
        .Where(file => extensions.Contains(Path.GetExtension(file).ToLowerInvariant()));

        Console.WriteLine("Computing file hashes...");
        foreach (string filePath in files)
        {
            // Create AudioFile object
            string fileHash = GetFileHash(filePath);

            // Append AudioFile in list
            if (fileMap.TryGetValue(fileHash, out List<string>? value))
            {
                value.Add(filePath);
            }
            else
            {
                fileMap[fileHash] = [filePath];
            }
        }

        Console.WriteLine("Computing duplicate...");
        using (StreamWriter streamWriter = new StreamWriter(outputFilePath))
        {
            foreach (var fileHashDict in fileMap)
            {
                if (fileHashDict.Value.Count > 1)
                {
                    string duplicateFiles = string.Join("\n", fileHashDict.Value);
                    streamWriter.WriteLine($"\nDuplicate files with hash {fileHashDict.Key}:\n{duplicateFiles}\n");
                }
            }
        }

        Console.WriteLine($"Text has been written to {outputFilePath}");
    }
}
