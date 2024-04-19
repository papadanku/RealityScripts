
using System.Collections;
using System.Net.Http.Headers;
using System.Text;

class Program
{
    static private void PrintMenuPrompt(string path)
    {
        // Create the new apps
        Application[] apps =
        [
            new AI(path),
            new Kits(path),
            new Shaders(path),
            new FileManager(path)
        ];

        // Create menu options
        Dictionary<int, string> menuOptions = new()
        {
            { 0, "AI" },
            { 1, "Kits" },
            { 2, "Shaders" },
            { 3, "FileManager" }
        };

        int appChoice = Application.GetChoiceIndex(menuOptions, "Welcome to RealityScipts!\nSelect the following apps:");

        // Execute the chosen app
        apps[appChoice].Execute();

        // Keep the app alive
        Console.WriteLine("Press enter to exit the app.");
        Console.ReadLine();
    }

    static void Main()
    {
        PrintMenuPrompt(@"D:\Program Files (x86)\Project Reality\Project Reality BF2\mods\pr_repo");
    }
}
