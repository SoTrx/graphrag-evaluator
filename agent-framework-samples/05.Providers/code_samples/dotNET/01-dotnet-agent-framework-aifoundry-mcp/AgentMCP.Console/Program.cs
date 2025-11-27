using ModelContextProtocol.Client;

using System;
using System.Linq;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;

using DotNetEnv;

Env.Load("./.env");

var azure_foundry_endpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT") ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
var azure_foundry_model_id = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-4.1-mini";

var persistentAgentsClient = new PersistentAgentsClient(azure_foundry_endpoint, new AzureCliCredential());

MCPToolDefinition mcpTool = new("mslearnmcp", "https://learn.microsoft.com/api/mcp");
string searchMSLearn = "searchmslearn";
mcpTool.AllowedTools.Add(searchMSLearn);

var agentModel = await persistentAgentsClient.Administration.CreateAgentAsync(
            model:azure_foundry_model_id,
            name: "MSLearnMCPAgent",
            instructions: "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
            tools: [mcpTool]
            );

AIAgent agent = await persistentAgentsClient.GetAIAgentAsync(agentModel.Value.Id);

Console.WriteLine($"Created agent with ID: {agent.Id}");

IMcpClient mcpClient = await McpClientFactory.CreateAsync(
    new SseClientTransport(new SseClientTransportOptions()
    {
        Endpoint = new Uri("https://learn.microsoft.com/api/mcp")
    })
);

IList<McpClientTool> tools = await mcpClient.ListToolsAsync();

Console.WriteLine("Available tools:");
foreach (var tool in tools)
{
    Console.WriteLine($"  {tool.Name}: {tool.Description}");
}

AgentThread thread = agent.GetNewThread();

ChatMessage userMessage = new ChatMessage(ChatRole.User, "What is Foundry Local?");


var chatOptions = new ChatClientAgentRunOptions
{
    ChatOptions = new ChatOptions
    {
        Tools = [.. tools]
    }
};

Console.WriteLine(await agent.RunAsync("What's Foundry Local?", thread, chatOptions));
