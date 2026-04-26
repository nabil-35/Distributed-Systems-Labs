\# Student:  mohamed nabil se3

\---



\## Lab A – Redis Replication (Master-Replica Setup)



\### What This Lab Does

This lab sets up a Redis replication cluster using Docker Compose, consisting of one \*\*master\*\* node and two \*\*replica\*\* nodes. The master accepts both reads and writes, while the replicas sync data from the master automatically and serve read requests.



\### Architecture Overview

```

redis-master  (port 6379)

&#x20;   ├── redis-replica-1  (port 6380)

&#x20;   └── redis-replica-2  (port 6381)

```

All nodes communicate over a shared Docker bridge network (`redis-network`) and use persistent volumes with AOF (Append-Only File) enabled.



\### Observations

\- Replicas connected to the master automatically on startup via the `--replicaof` flag

\- Data written to the master appeared on both replicas with negligible delay

\- AOF persistence (`--appendonly yes`) ensured data survived container restarts

\- Each node has its own isolated volume, preventing data conflicts

\- The `depends\_on` directive ensured replicas only started after the master was ready



\### Key Concepts Learned

\- \*\*Master-Replica Replication:\*\* Writes go to master only; replicas are read-only mirrors

\- \*\*AOF Persistence:\*\* Every write operation is logged to disk, enabling crash recovery

\- \*\*Docker Networking:\*\* A bridge network allows containers to resolve each other by name (e.g., `redis-master`)

\- \*\*Replication Lag:\*\* Under load, replicas may be slightly behind the master — relevant for consistency guarantees

\- \*\*Read Scalability:\*\* Replicas offload read traffic from the master, improving throughput



\### Challenges Faced

\- Replicas starting before the master was fully ready caused connection errors — solved with `depends\_on`

\- Understanding the difference between replication (availability) and persistence (durability)

\- Verifying replication was working required connecting to each container separately via `redis-cli`



\### Conclusion

Redis replication is a foundational pattern for building highly available caching and data layers. The master-replica model trades strong consistency for high read throughput and is widely used in production systems where eventual consistency is acceptable.



\---



\## Lab B – etcd Distributed Key-Value Store (3-Node Cluster)



\### What This Lab Does

This lab deploys a 3-node \*\*etcd\*\* cluster using Docker Compose. etcd is a strongly consistent, distributed key-value store that uses the \*\*Raft consensus algorithm\*\* to maintain agreement across nodes. It is commonly used as the backbone for distributed system coordination (e.g., Kubernetes uses etcd for cluster state).



\### Architecture Overview

```

etcd1 (client: 2379, peer: 2380)

etcd2 (client: 2381, peer: 2382)

etcd3 (client: 2383, peer: 2384)

&#x20;        ↕ Raft Consensus ↕

&#x20;    All nodes elect one Leader

```

All nodes are initialized with `ETCD\_INITIAL\_CLUSTER\_STATE=new` and share the same cluster token (`etcd-cluster-lab2`).



\### Observations

\- The cluster automatically elected a \*\*leader\*\* among the three nodes using Raft

\- Any node could serve client reads, but writes were coordinated through the leader

\- Removing one node still allowed the cluster to function (quorum = 2 of 3)

\- All nodes had identical `ETCD\_INITIAL\_CLUSTER` configuration, enabling peer discovery

\- `ALLOW\_NONE\_AUTHENTICATION=yes` simplified setup for the lab environment



\### Key Concepts Learned

\- \*\*Raft Consensus:\*\* A leader is elected; all writes go through it and are replicated to a majority before being committed

\- \*\*Quorum:\*\* With 3 nodes, the cluster tolerates 1 failure (majority = 2)

\- \*\*Strong Consistency:\*\* Unlike Redis replication, etcd guarantees linearizable reads — no stale data

\- \*\*Peer URLs vs Client URLs:\*\* Peers communicate on port 2380 (internal); clients connect on port 2379 (external)

\- \*\*Cluster Token:\*\* Prevents nodes from accidentally joining the wrong cluster



\### Challenges Faced

\- Misconfiguring `ETCD\_INITIAL\_CLUSTER` caused nodes to fail to find peers — exact name matching with service names was required

\- Understanding the difference between peer ports (inter-node) and client ports (application-facing)

\- Distinguishing etcd's strong consistency model from Redis's eventual consistency model



\### Conclusion

etcd demonstrates how distributed consensus enables reliable coordination in systems where correctness matters more than raw speed. While more complex than Redis replication, etcd's Raft-based approach guarantees that all nodes agree on the same state — making it ideal for configuration management, service discovery, and leader election in distributed systems.



\---



\## Comparative Summary



| Feature | Redis Replication | etcd Cluster |

|---|---|---|

| Consistency Model | Eventual | Strong (linearizable) |

| Write Handling | Master only | Leader (via Raft) |

| Fault Tolerance | Replicas serve reads if master fails | Tolerates minority node failures |

| Primary Use Case | Caching, fast reads | Coordination, configuration |

| Consensus Algorithm | None (async replication) | Raft |

| Data Persistence | AOF / RDB | WAL (Write-Ahead Log) |



Both systems are complementary — Redis for high-performance data storage, etcd for reliable distributed coordination.



