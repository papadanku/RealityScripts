
using System.Text;

class Program
{
    private static int GetChoiceIndex(Application[] apps, string initialPrompt)
    {
        // Build prompt string
        StringBuilder prompt = new();
        prompt.AppendLine(initialPrompt);
        for (int i = 0; i < apps.Length; i++)
        {
            prompt.AppendLine($"{i}: {apps[i].Description}");
        }

        // Print prompt to console
        Console.WriteLine(prompt);

        // Allow the user to choose between N options
        int choice;
        do
        {
            Console.Write("Enter your choice: ");
            string? response = Console.ReadLine();
            choice = int.Parse(response);
        } while (choice < 0 || choice > apps.Length);

        return choice;
    }

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

        // Execute the chosen app
        int appChoice = GetChoiceIndex(apps, "\nWelcome to RealityScipts!\n\nSelect the following apps:");
        apps[appChoice].Execute();

        // Keep the app alive
        Console.Write("Press enter to exit the app.");
        Console.ReadLine();
    }

    static void Main()
    {
        string repoDirPath;
        do
        {
            Console.Write("Enter repository directory path: ");
            repoDirPath = Console.ReadLine();
        } while(!Path.Exists(repoDirPath));

        PrintMenuPrompt(repoDirPath);
    }
}
