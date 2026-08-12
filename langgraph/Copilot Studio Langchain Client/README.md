# LangChain connected to Copilot Studio Agent

## 1.  Create a Copilot Studio Agent
Add a knowledge Source:<br/>
<img width="1799" height="584" alt="image" src="https://github.com/user-attachments/assets/71c79ae1-da68-4008-a57a-7bfac8d87928" /><br/>

Copy the Connection String from:<br/>
<img width="2421" height="1272" alt="image" src="https://github.com/user-attachments/assets/d5b41b7a-83f2-4874-bd40-1f556a06bf86" /><br/>

## 2.  Create App Registration from Azure Portal
<img width="2239" height="1049" alt="image" src="https://github.com/user-attachments/assets/9b848a3c-4298-4d76-bfe4-9321147bbd39" /><br/>
Add these API Permission:<br/>
<img width="2252" height="1277" alt="image" src="https://github.com/user-attachments/assets/df3c4511-5784-461b-8114-1640710bf8f3" /><br/>

## 3. Implement LangChain connected to Copilot Studio Agent 
.env file is like:
```
# Copilot Studio > Channels > Native app > Microsoft 365 Agents SDK
COPILOT_STUDIO_DIRECT_CONNECT_URL=https://example.environment.api.powerplatform.com/copilotstudio/dataverse-backed/authenticated/bots/your-agent/conversations?api-version=2022-03-01-preview
COPILOT_STUDIO_TENANT_ID=your-microsoft-entra-tenant-id
COPILOT_STUDIO_CLIENT_ID=your-public-client-application-id
```

