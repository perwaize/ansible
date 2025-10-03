# cluster_app_report.py
# Run with: wsadmin.sh -lang jython -f cluster_app_report.py

import socket
hostname = socket.gethostname()

clusters = AdminConfig.list("ServerCluster").splitlines()

for cluster in clusters:
    cname = AdminConfig.showAttribute(cluster, "name")
    members = AdminConfig.list("ClusterMember", cluster).splitlines()
    jvm_count = len(members)

    # Distinct nodes
    nodes = set()
    for member in members:
        node = AdminConfig.showAttribute(member, "nodeName")
        nodes.add(node)
    node_count = len(nodes)

    # Count apps targeted to this cluster
    apps = AdminApp.list().splitlines()
    deployed_apps = []
    for app in apps:
        targets = AdminApp.view(app, "-MapModulesToServers").splitlines()
        for t in targets:
            if cname in t:
                deployed_apps.append(app)
                break
    app_count = len(deployed_apps)

    # Adjusted column order
    print "%s, %s, %d, %d, %d" % (hostname, cname, node_count, jvm_count, app_count)
