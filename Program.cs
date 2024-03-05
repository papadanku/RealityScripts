
using System.Text;

class Program
{
    static private string GetRepoPath()
    {
        Console.WriteLine("Please enter your repository's path: ");
        return Console.ReadLine().Trim();
    }

    /// <summary>
    /// Main function for selecting applications
    /// </summary>
    static private void SelectApplication(string path)
    {
        // Create the new apps
        Application[] apps =
        [
            new AI(path),
            new Kits(path),
            new Shaders(path),
        ];

        // Create menu options
        string[] menuOptions =
        [
            "",
            "0: AI",
            "1: Kits",
            "2: Shaders",
        ];
        string prompt = string.Join("\n\t", menuOptions);

        // Application selection loop
        while (true)
        {
            // Allow the user to choose between N options
            int choice = -1;
            string? userResponse;

            // Turn userResponse into a number
            while (choice < 0 || choice > apps.Length)
            {
                // List the available choices
                Console.WriteLine($"Choose your Application:\n{prompt}");

                // Get user's choice
                userResponse = Console.ReadLine().ToLower().Trim();
                choice = int.Parse(userResponse);
            }

            // Execute the selected application
            apps[choice].Execute();

            // Prompt the user if they are done with the application
            Console.WriteLine(@"Do you want to stop using the application? Press ""y"" if so.");
            userResponse = Console.ReadLine().ToLower().Trim();
            if (userResponse == "y")
            {
                break;
            }
        }

        // Keep the app alive
        Console.WriteLine("Press enter to exit the app.");
        string exit = Console.ReadLine();
    }

    static void Main()
    {
        Console.WriteLine("Welcome to RealityScipts!");

        // Get Project Reality's repo path
        string RepoPath = GetRepoPath();

        // Undergo application selection
        SelectApplication(RepoPath);
    }
}
