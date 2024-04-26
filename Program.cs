
using System.Collections;
using System.Net.Http.Headers;
using System.Security.Cryptography;
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
            new FileManager(path),
        ];

        // Create menu options
        Dictionary<int, string> menuOptions = [];
        for (int i = 0; i <= apps.Length; i++)
        {
            menuOptions[i+1] = apps[i].Description;
        }

        int appChoice = Application.GetChoiceIndex(menuOptions, "\nWelcome to RealityScipts!\n\nSelect the following apps:");

        // Execute the chosen app
        apps[appChoice].Execute();

        // Keep the app alive
        Console.Write("Press enter to exit the app.");
        Console.ReadLine();
    }

    static void Main()
    {
        Console.Write("Enter repository directory path: ");
        string repoDirPath = Console.ReadLine();
        PrintMenuPrompt(repoDirPath);
    }
}
