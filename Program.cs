
using System.Text;

class Program
{
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
        {
            "",
            "0: AI",
            "1: Kits",
            "2: Shaders",
        };

        StringBuilder prompt = new();
        prompt.AppendLine("Here are the following apps:");
        prompt.AppendJoin("\n\t", menuOptions);

        // Prompt the user to select a directory
        Console.WriteLine(prompt);

        // Allow the user to choose between N options
        int choice;
        do
        {
            Console.WriteLine("Enter your choice: ");
            string? response = Console.ReadLine();
            choice = int.Parse(response);
        } while (!(choice >= 0 && choice < apps.Length));

        // Execute the chosen app
        apps[choice].Execute();

        // Keep the app alive
        Console.WriteLine("Press enter to exit the app.");
        string endApp = Console.ReadLine();
    }

    static private string GetRepoPath()
    {
        Console.WriteLine("Please enter your repository's path: ");
        return Console.ReadLine().Trim();
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
