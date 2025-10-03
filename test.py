# cluster_app_report.py
# Run with: wsadmin.sh -lang jython -f cluster_app_report.py

clusters = AdminConfig.list("ServerCluster").splitlines()

print "Total Clusters: %s" % len(clusters)

for cluster in clusters:
    cname = AdminConfig.showAttribute(cluster, "name")
    members = AdminConfig.list("ClusterMember", cluster).splitlines()
    apps = AdminApp.list().splitlines()

    # Find apps targeted to this cluster
    deployed_apps = []
    for app in apps:
        targets = AdminApp.view(app, "-MapModulesToServers").splitlines()
        for t in targets:
            if cname in t:
                deployed_apps.append(app)
                break

    print "\nCluster: %s" % cname
    print "  JVM count: %s" % len(members)
    print "  Apps deployed: %s" % len(deployed_apps)
