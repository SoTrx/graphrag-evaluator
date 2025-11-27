using Azure.Identity;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using OpenAI.Responses;

using Microsoft.Agents.AI.Workflows;
using Microsoft.Agents.AI.Workflows.Declarative;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;


internal sealed class Program
{
    public static async Task Main(string[] args)
    {
        // IConfiguration configuration = Application.InitializeConfig();
        Uri foundryEndpoint = new("https://kinfey-ai-ignite-demo-resource.services.ai.azure.com/api/projects/kinfey-ai-ignite-demo");

        WorkflowFactory workflowFactory = new("Your workflow.yaml path", foundryEndpoint);
        WorkflowRunner runner = new();
        await runner.ExecuteAsync(workflowFactory.CreateWorkflow, "junior developer");    
    }
}
    

