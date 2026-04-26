Lab 1 – Reflection

Student Name: Mohamed Nabil

What This Lab Does

This lab measures the Round-Trip Latency of a TCP connection between a client and server running on the same machine (loopback). The server echoes back any message it receives, and the client measures the time for each round-trip.

Observations

•	Local TCP latency was extremely low (under 1 ms typically)

•	There was some variance due to OS scheduling and system load

•	The distribution was roughly normal with a slight right tail (occasional spikes)

•	P99 was noticeably higher than the mean, showing tail latency behavior

Key Concepts Learned

•	RTT (Round-Trip Time): Time for a packet to go from sender → receiver → back

•	Tail latency: P95/P99 percentiles show worst-case latency, important for SLAs

•	TCP overhead: Even on loopback, TCP adds measurable latency vs raw memory access

•	time.perf\_counter(): More accurate than time.time() for short intervals

Challenges Faced

•	Initial attempts using time.time() gave inconsistent results; switching to time.perf\_counter() solved this

•	Making sure the server was running before starting the client

Conclusion

Latency measurement is a fundamental skill in distributed systems. Even small differences in latency (a few ms) can have a large impact at scale when millions of requests are made per second.



