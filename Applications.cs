
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

abstract class Application(string path)
{
    public abstract string Description { get; set; }
    public string RepoPath = path;

    public abstract void Execute();

    public static int GetOptionIndex(Dictionary<int, string> options, string initialPrompt)
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
/// Application for processing AI templates.
/// </summary>
class AI : Application
{
    public override string Description { get; set; } = "AI Kit Checking";
    private Dictionary<string, HashSet<string>> _filePaths;
    private HashSet<string> _aiTemplates;

    public AI(string path) : base(path)
    {
        _filePaths = new();
        _filePaths[".ai"] = [];
        _filePaths[".tweak"] = [];
        _aiTemplates = [];
    }

    public override void Execute()
    {
        Console.WriteLine("\nStarting application...\n");
        GetDirectories();
        GetTemplates();
        CheckTemplates();
    }

    private void GetDirectories()
    {
        List<string> searchDirectories = [];

        // Build available options
        Dictionary<int, string> options = new()
        {
            { 1, "Vehicles" },
            { 2, "Weapons" },
            { 3, "Objects" },
            { 4, "Kits" }
        };

        int appChoice = GetOptionIndex(options, "\nCheck AI Templates for:");
        switch (appChoice)
        {
            case 1:
                searchDirectories.Add("vehicles");
                break;
            case 2:
                searchDirectories.Add("weapons");
                break;
            case 3:
                searchDirectories.Add("staticobjects");
                searchDirectories.Add("dynamicobjects");
                break;
            case 4:
                searchDirectories.Add("kits");
                break;
        }

        // Initialize file paths
        HashSet<string> allFilePaths = [];
        HashSet<string> fileExtensions = [".ai", ".tweak"];

        // Get files from selected directories
        foreach (string directory in searchDirectories)
        {
            string searchPath = Path.Combine(RepoPath, "objects", directory);
            allFilePaths.UnionWith(Directory.GetFiles(searchPath, "*", SearchOption.AllDirectories));
        }

        // Group filepaths by extension
        foreach (string filePath in allFilePaths)
        {
            string fileExtension = Path.GetExtension(filePath);
            if (fileExtensions.Contains(fileExtension))
            {
                _filePaths[fileExtension].Add(filePath);
            }
        }
    }

    public void GetTemplates()
    {
        // Let the user know that the app is working
        Console.WriteLine("Gathering AI templates...");

        foreach (string path in _filePaths[".ai"])
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

        foreach (string path in _filePaths[".tweak"])
        {
            string fileText = File.ReadAllText(path);
            MatchCollection templates = Regex.Matches(fileText, @"(?:\w+\.aiTemplate )(\w+)", RegexOptions.Compiled);

            foreach (Match template in templates)
            {
                string aiTemplate = template.Groups[1].ToString();
                if (!_aiTemplates.Contains(aiTemplate))
                {
                    Console.WriteLine($"\n{template} has missing template!\n\t{path}");
                }
            }
        }
    }
}

/// <summary>
/// Application for processing kit templates.
/// </summary>
class Kits : Application
{
    public override string Description { get; set; } = "Check Pre-Allocated Kits";
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
/// Application for processing shader files.
/// </summary>
class Shaders : Application
{
    public override string Description { get; set; } = "Display Shader Techniques";
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
    public override string Description { get; set; } = "FileManager";

    public override void Execute()
    {
        PrintDuplicateFiles();
    }

    private void PrintDuplicateFiles()
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

        int appChoice = GetOptionIndex(menuOptions, "Check Duplicate Files for:");
        FindDuplicateFiles(RepoPath, fileExtensions[appChoice], outputFilePath);
    }

    /// <summary>
    /// Get the hash of a given file.
    /// </summary>
    private static string GetFileHash(string filePath)
    {
        // Initialize SHA256 filestream
        using FileStream fileStream = File.OpenRead(filePath);

        // Compute the fileStream's hash value
        byte[] fileHash = MD5.HashData(fileStream);

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

        // Compute and organize file hashes for each filePath
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
        using (StreamWriter streamWriter = new(outputFilePath))
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
