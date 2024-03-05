
using System.Text;
using System.Text.RegularExpressions;

abstract class Application(string path)
{
    public string RepoPath = path;

    public abstract void Execute();
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
        GetDirectories();
        GetTemplates();
        CheckTemplates();
    }

    private void GetDirectories()
    {
        // Build available options
        string[] menuOptions =
        [
            "0: Vehicles",
            "1: Weapons",
            "2: Objects",
            "3: Kits"
        ];

        string prompt = string.Join("\n", menuOptions);

        // Allow the user to choose between N options
        int choice = -1;
        string? userResponse;

        while (choice < 0 || choice > menuOptions.Length)
        {
            // List the available choices
            Console.WriteLine($"Choose your Application:\n{prompt}");

            // Get user's choice
            userResponse = Console.ReadLine().ToLower().Trim();
            choice = int.Parse(userResponse);
        }

        switch (choice)
        {
            case 0:
                _searchDirectories.Add("vehicles");
                break;
            case 1:
                _searchDirectories.Add("weapons");
                break;
            case 2:
                _searchDirectories.Add("staticobjects");
                _searchDirectories.Add("dynamicobjects");
                break;
            case 3:
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
        if (!missingKits.Any())
        {
            Console.WriteLine($"{variant}: No missing kits");
        }
        else
        {
            Console.WriteLine($"{variant}:\n\t{string.Join($"\n\t", missingKits)}");
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
