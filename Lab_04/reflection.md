Lab 4 – Reflection Report

\# Student: mohamed nabil se3

1\. Benefits of Microservices over a Monolith

•	Independent Deployment: Each service is deployed independently. Updating the product catalog requires redeploying only product-service, with no impact on order-service.

•	Independent Scaling: If order-service receives heavier traffic, it can be scaled up on its own without scaling product-service unnecessarily.

•	Technology Flexibility: Each service maintains its own requirements.txt and can use different libraries or even different programming languages in the future.

•	Fault Isolation: When product-service failed, order-service returned a 503 error gracefully instead of crashing entirely — failures remain contained.

2\. New Complexities Introduced by Splitting Services

•	Network Dependency: order-service now depends on network calls to product-service. Unlike in-process calls, network calls can fail or be slow.

•	Service Discovery: order-service must know the address of product-service. This was solved using environment variables rather than hardcoded values.

•	Distributed Failure Handling: Timeout and retry logic had to be added inside fetch\_product() to handle partial failures gracefully.

•	More Containers to Manage: The system now involves two containers, two Dockerfiles, and a Docker Compose file, increasing operational overhead.

3\. Impact of Increased Network Latency or Slow Services

order-service enforces a 2-second timeout. If product-service takes longer to respond, the request fails immediately.

The retry mechanism (2 retries with a 1-second delay between each) means a slow product-service could cause order-service to take up to 6 seconds per request.

Under high load, slow responses can cascade — all order requests begin queuing and timing out simultaneously. This is known as a cascading failure.

A circuit breaker pattern would mitigate this by detecting repeated failures and short-circuiting calls to the failing service early, preventing resource exhaustion.

4\. Visible 12-Factor App Principles

•	Factor III – Config: PRODUCT\_SERVICE\_URL is read from environment variables rather than hardcoded in source code.

•	Factor VI – Processes: Both services are stateless processes. No session or mutable state is stored locally between requests.

•	Factor VII – Port Binding: Each service binds to its own port (5001 and 5002) and is fully self-contained.

•	Factor IX – Disposability: Both services start quickly and shut down cleanly, supported by the restart: unless-stopped policy in Docker Compose.

•	Factor XI – Logs: Both services write logs to stdout, which Docker captures and makes available via docker compose logs.

Conclusion

This lab demonstrated how microservices deliver flexibility and fault isolation at the cost of added network complexity. The combination of Docker and Docker Compose made it straightforward to containerize and orchestrate both services locally, simulating a real cloud-native deployment. The trade-offs between distributed resilience and operational complexity became tangible through hands-on implementation.



