
using System.Collections;
using System.Net.Http.Headers;
using System.Text;

class Program
{
    static private void PrintMenuPrompt(string path)
    {
        // Create the new apps
        Dictionary<int, Application> apps = new()
        {
            { 1, new AI(path) },
            { 2, new Kits(path) },
            { 3, new Shaders(path) },
            { 4, new FileManager(path) },
        };

        // Create menu options
        Dictionary<int, string> menuOptions = new()
        {
            { 1, "AI" },
            { 2, "Check Pre-Allocated Kits" },
            { 3, "Display Shader Techniques" },
            { 4, "FileManager" }
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
