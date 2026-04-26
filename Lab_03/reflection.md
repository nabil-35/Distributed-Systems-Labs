Lab 3 – Reflection

Student: Mohamed Nabil se3



What This Lab Covers

This lab deploys a containerized Python Flask application on Kubernetes using Minikube. A Deployment with 3 replicas is created and exposed via a Service, demonstrating self-healing behavior and declarative infrastructure management.

Key Kubernetes Concepts

Pods

The smallest deployable unit in Kubernetes. Each Pod runs one instance of the Flask application. Three Pods were deployed to enable load distribution and redundancy across the cluster.

Deployments

A Deployment manages the desired state of the application — in this case, 3 replicas. If a Pod fails or is deleted, the Deployment controller detects the drift from desired state and automatically provisions a replacement.

Services

A Service provides a stable, persistent network endpoint for a set of Pods. Clients connect to the Service IP, and Kubernetes transparently load-balances traffic across all healthy Pod instances.

ConfigMap

ConfigMaps externalize configuration values — such as APP\_VERSION and ENVIRONMENT — from the container image itself. This follows the 12-factor app methodology, keeping code and config cleanly separated.

Self-Healing Demonstration

When a Pod was manually deleted using kubectl delete pod <name>, Kubernetes immediately detected that the actual running state (2 Pods) diverged from the declared desired state (3 Pods). Within seconds, the Deployment controller scheduled and launched a new replacement Pod — without any manual intervention.

Health Probes

•	Liveness Probe: Periodically checks whether the application is alive. If the probe fails, Kubernetes restarts the container automatically.

•	Readiness Probe: Determines whether the application is ready to serve traffic. Pods that fail this check are temporarily removed from the Service load balancer.

What I Learned

•	Kubernetes manages the full application lifecycle automatically, including scheduling, scaling, and recovery

•	Declarative YAML configuration makes deployments reproducible and version-controllable

•	Health probes enable automatic recovery without operator involvement

•	Horizontal scaling is as straightforward as updating the replicas field in the Deployment spec

•	The separation of Pods, Deployments, and Services reflects a clean layered architecture for distributed applications

Conclusion

Kubernetes abstracts away the complexity of managing distributed containerized applications. Through this lab, the core control loop — observe, diff, reconcile — became tangible: Kubernetes continuously compares actual state to desired state and acts to close the gap. This makes it a powerful platform for building resilient, self-healing systems at scale.



