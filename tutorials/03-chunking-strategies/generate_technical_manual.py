"""Generate a ~50 page Kubernetes Operations Manual PDF using reportlab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)

OUTPUT_DIR = Path(__file__).parent / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "technical_manual.pdf"

PAGE_W, PAGE_H = A4


def build_styles():
    ss = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title2", parent=ss["Title"], fontSize=28, spaceAfter=20
        ),
        "subtitle": ParagraphStyle(
            "Subtitle2", parent=ss["Title"], fontSize=16, spaceAfter=40
        ),
        "h1": ParagraphStyle(
            "H1", parent=ss["Heading1"], fontSize=20, spaceBefore=24, spaceAfter=12
        ),
        "h2": ParagraphStyle(
            "H2", parent=ss["Heading2"], fontSize=14, spaceBefore=16, spaceAfter=8
        ),
        "h3": ParagraphStyle(
            "H3", parent=ss["Heading3"], fontSize=12, spaceBefore=12, spaceAfter=6
        ),
        "body": ParagraphStyle(
            "Body2", parent=ss["BodyText"], fontSize=10, leading=14, spaceAfter=6
        ),
        "bullet": ParagraphStyle(
            "Bullet2",
            parent=ss["BodyText"],
            fontSize=10,
            leading=14,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4,
        ),
        "numbered": ParagraphStyle(
            "Numbered2",
            parent=ss["BodyText"],
            fontSize=10,
            leading=14,
            leftIndent=24,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "Code2",
            fontName="Courier",
            fontSize=8,
            leading=10,
            leftIndent=12,
            spaceBefore=6,
            spaceAfter=6,
            backColor=colors.Color(0.95, 0.95, 0.95),
        ),
        "warning": ParagraphStyle(
            "Warning2",
            parent=ss["BodyText"],
            fontSize=10,
            leading=14,
            leftIndent=24,
            borderWidth=1,
            borderColor=colors.orange,
            borderPadding=6,
            spaceBefore=8,
            spaceAfter=8,
            backColor=colors.Color(1.0, 0.97, 0.9),
        ),
        "note": ParagraphStyle(
            "Note2",
            parent=ss["BodyText"],
            fontSize=10,
            leading=14,
            leftIndent=24,
            borderWidth=1,
            borderColor=colors.blue,
            borderPadding=6,
            spaceBefore=8,
            spaceAfter=8,
            backColor=colors.Color(0.93, 0.95, 1.0),
        ),
        "toc": ParagraphStyle(
            "TOC2", parent=ss["BodyText"], fontSize=11, leading=18, leftIndent=12
        ),
        "toc_section": ParagraphStyle(
            "TOCSec",
            parent=ss["BodyText"],
            fontSize=10,
            leading=16,
            leftIndent=30,
        ),
    }
    return styles


def make_table(data, col_widths=None):
    if col_widths is None:
        col_widths = [4 * cm] * len(data[0])
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.5)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.97)]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def code_block(text):
    return Preformatted(text, style=ParagraphStyle(
        "PreCode",
        fontName="Courier",
        fontSize=8,
        leading=10,
        leftIndent=12,
        spaceBefore=6,
        spaceAfter=6,
        backColor=colors.Color(0.95, 0.95, 0.95),
    ))


def build_title_page(styles):
    elements = []
    elements.append(Spacer(1, 6 * cm))
    elements.append(Paragraph("Kubernetes Operations Manual", styles["title"]))
    elements.append(Paragraph("Version 2.1", styles["subtitle"]))
    elements.append(Spacer(1, 2 * cm))
    elements.append(Paragraph("Infrastructure Engineering Team", styles["body"]))
    elements.append(Paragraph("Last Updated: June 2026", styles["body"]))
    elements.append(Paragraph("Classification: Internal Use Only", styles["body"]))
    elements.append(Spacer(1, 3 * cm))
    elements.append(
        Paragraph(
            "This document covers the complete lifecycle of Kubernetes cluster "
            "operations including installation, configuration, monitoring, "
            "troubleshooting, backup/recovery, and security hardening procedures.",
            styles["body"],
        )
    )
    elements.append(PageBreak())
    return elements


def build_toc(styles):
    elements = []
    elements.append(Paragraph("Table of Contents", styles["h1"]))
    elements.append(Spacer(1, 0.5 * cm))
    sections = [
        ("1", "Prerequisites", ["1.1 Hardware Requirements", "1.2 Software Dependencies", "1.3 Network Requirements", "1.4 Access and Credentials"]),
        ("2", "Installation", ["2.1 Cluster Bootstrap", "2.2 Control Plane Setup", "2.3 Worker Node Join", "2.4 Verification"]),
        ("3", "Configuration", ["3.1 Cluster Configuration", "3.2 Networking", "3.3 Storage Classes", "3.4 Resource Quotas"]),
        ("4", "Deployments & Services", ["4.1 Deployment Strategies", "4.2 Service Types", "4.3 Ingress Configuration", "4.4 Helm Charts"]),
        ("5", "Monitoring & Observability", ["5.1 Prometheus Setup", "5.2 Grafana Dashboards", "5.3 Alert Rules", "5.4 Log Aggregation"]),
        ("6", "Troubleshooting", ["6.1 Pod Failures", "6.2 Network Issues", "6.3 Storage Problems", "6.4 Performance Degradation"]),
        ("7", "Backup & Recovery", ["7.1 etcd Backup", "7.2 Persistent Volume Backup", "7.3 Disaster Recovery", "7.4 Verification Procedures"]),
        ("8", "Security Hardening", ["8.1 RBAC Configuration", "8.2 Network Policies", "8.3 Pod Security Standards", "8.4 Secret Management"]),
    ]
    appendices = [
        ("A", "kubectl Command Reference", ["A.1 Cluster Management", "A.2 Workload Management", "A.3 Networking Commands", "A.4 Storage Commands", "A.5 RBAC and Security Commands"]),
        ("B", "Operational Runbooks", ["B.1 Node Not Ready", "B.2 High API Server Latency", "B.3 Certificate Expiry"]),
        ("C", "Configuration Templates", ["C.1 Production-Ready Deployment", "C.2 Environment Variables Reference", "C.3 Horizontal Pod Autoscaler", "C.4 PodDisruptionBudget"]),
        ("D", "Cluster Upgrade Procedures", ["D.1 Pre-Upgrade Checklist", "D.2 Control Plane Upgrade", "D.3 Worker Node Upgrade", "D.4 Post-Upgrade Verification"]),
        ("E", "Disaster Recovery Scenarios", ["E.1 Complete Control Plane Loss", "E.2 Single Worker Node Failure", "E.3 etcd Data Corruption", "E.4 Network Partition", "E.5 Recovery Time Summary"]),
    ]
    for num, title, subs in sections:
        elements.append(Paragraph(f"<b>{num}. {title}</b>", styles["toc"]))
        for sub in subs:
            elements.append(Paragraph(sub, styles["toc_section"]))
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(Paragraph("<b>Appendices</b>", styles["toc"]))
    for num, title, subs in appendices:
        elements.append(Paragraph(f"<b>Appendix {num}. {title}</b>", styles["toc"]))
        for sub in subs:
            elements.append(Paragraph(sub, styles["toc_section"]))
    elements.append(PageBreak())
    return elements


def section_prerequisites(styles):
    e = []
    e.append(Paragraph("1. Prerequisites", styles["h1"]))
    e.append(Paragraph(
        "Before beginning the Kubernetes cluster installation, ensure all prerequisites "
        "are met. Failure to meet these requirements will result in installation failures "
        "or degraded cluster performance.",
        styles["body"],
    ))

    e.append(Paragraph("1.1 Hardware Requirements", styles["h2"]))
    e.append(Paragraph(
        "Each node in the cluster must meet the following minimum hardware specifications. "
        "Production deployments should exceed these minimums by at least 2x.",
        styles["body"],
    ))
    e.append(make_table([
        ["Component", "Control Plane", "Worker Node", "etcd Node"],
        ["CPU Cores", "4 cores min", "8 cores min", "4 cores min"],
        ["RAM", "16 GB", "32 GB", "16 GB"],
        ["Disk (SSD)", "100 GB", "200 GB", "100 GB (IOPS>3000)"],
        ["Network", "1 Gbps", "10 Gbps", "1 Gbps"],
    ], col_widths=[3.5*cm, 3.5*cm, 3.5*cm, 4*cm]))
    e.append(Spacer(1, 0.5*cm))

    for item in [
        "All nodes must have consistent time synchronization (NTP/chrony)",
        "Swap must be disabled on all nodes (swapoff -a)",
        "Kernel version 5.4+ is required for eBPF-based networking",
        "UEFI Secure Boot must be disabled or properly configured",
        "Hardware watchdog timer should be available for kubelet",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>WARNING:</b> Running Kubernetes on nodes with less than 4 CPU cores will "
        "cause the API server to become unresponsive under moderate load. The scheduler "
        "requires dedicated CPU cycles and will starve other components.",
        styles["warning"],
    ))

    e.append(Paragraph("1.2 Software Dependencies", styles["h2"]))
    e.append(Paragraph(
        "Install the following software on all nodes before proceeding. Version "
        "compatibility is critical - mismatched versions between nodes cause TLS failures.",
        styles["body"],
    ))
    e.append(make_table([
        ["Software", "Minimum Version", "Recommended", "Notes"],
        ["Container Runtime", "containerd 1.7.x", "containerd 1.7.22", "CRI-compatible"],
        ["kubelet", "v1.29.0", "v1.30.2", "Match control plane"],
        ["kubeadm", "v1.29.0", "v1.30.2", "Bootstrap tool"],
        ["kubectl", "v1.29.0", "v1.30.2", "Client tool"],
        ["helm", "v3.14.0", "v3.15.3", "Package manager"],
    ], col_widths=[3.5*cm, 3.5*cm, 3.5*cm, 4*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Install containerd and configure it:", styles["body"]))
    e.append(code_block(
        "# Install containerd\n"
        "sudo apt-get update && sudo apt-get install -y containerd.io\n"
        "\n"
        "# Generate default config\n"
        "sudo mkdir -p /etc/containerd\n"
        "containerd config default | sudo tee /etc/containerd/config.toml\n"
        "\n"
        "# Enable SystemdCgroup\n"
        "sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' \\\n"
        "  /etc/containerd/config.toml\n"
        "\n"
        "# Restart containerd\n"
        "sudo systemctl restart containerd\n"
        "sudo systemctl enable containerd"
    ))

    e.append(Paragraph(
        "<b>NOTE:</b> Docker Engine is no longer supported as a container runtime "
        "since Kubernetes v1.24. Migrate to containerd or CRI-O. "
        "See Section 2.1 for migration steps.",
        styles["note"],
    ))

    e.append(Paragraph("1.3 Network Requirements", styles["h2"]))
    e.append(Paragraph(
        "Kubernetes requires specific network ports to be open between nodes. "
        "Firewall rules must permit bidirectional traffic on these ports.",
        styles["body"],
    ))
    e.append(make_table([
        ["Port Range", "Protocol", "Purpose", "Direction"],
        ["6443", "TCP", "Kubernetes API Server", "Inbound to control plane"],
        ["2379-2380", "TCP", "etcd client/peer", "Control plane internal"],
        ["10250", "TCP", "Kubelet API", "All nodes"],
        ["10259", "TCP", "kube-scheduler", "Control plane"],
        ["10257", "TCP", "kube-controller-manager", "Control plane"],
        ["30000-32767", "TCP", "NodePort Services", "Worker nodes inbound"],
    ], col_widths=[3*cm, 2.5*cm, 4.5*cm, 4.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    for item in [
        "Pod CIDR: 10.244.0.0/16 (default for Flannel) or 192.168.0.0/16 (Calico)",
        "Service CIDR: 10.96.0.0/12 (default)",
        "DNS resolution must work between all nodes (verify with nslookup)",
        "MTU must be consistent across all nodes (check with ip link show)",
        "No overlapping CIDRs with existing infrastructure networks",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(code_block(
        "# Verify network connectivity between nodes\n"
        "for node in node1 node2 node3; do\n"
        "  echo \"Testing $node...\"\n"
        "  nc -zv $node 6443 2>&1 | grep -q succeeded && echo \"OK\" || echo \"FAIL\"\n"
        "  nc -zv $node 10250 2>&1 | grep -q succeeded && echo \"OK\" || echo \"FAIL\"\n"
        "done\n"
        "\n"
        "# Verify DNS resolution\n"
        "nslookup kubernetes.default.svc.cluster.local"
    ))

    e.append(Paragraph("1.4 Access and Credentials", styles["h2"]))
    e.append(Paragraph(
        "The following credentials and access levels are required before installation:",
        styles["body"],
    ))
    for item in [
        "SSH access to all nodes with sudo/root privileges",
        "Container registry credentials (for private registries)",
        "TLS certificates for the API server (or use self-signed for dev)",
        "Cloud provider credentials (for cloud-managed load balancers)",
        "DNS zone management access (for external-dns integration)",
        "Vault/KMS access tokens (for secret encryption at rest)",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(code_block(
        "# Generate SSH key pair for node access\n"
        "ssh-keygen -t ed25519 -C \"k8s-admin\" -f ~/.ssh/k8s_admin\n"
        "\n"
        "# Distribute to all nodes\n"
        "for node in cp1 worker1 worker2 worker3; do\n"
        "  ssh-copy-id -i ~/.ssh/k8s_admin.pub admin@$node\n"
        "done\n"
        "\n"
        "# Verify access\n"
        "ansible all -m ping -i inventory.ini"
    ))
    e.append(Paragraph(
        "<b>WARNING:</b> Never store cluster admin credentials in version control. "
        "Use a secrets manager (HashiCorp Vault, AWS Secrets Manager) for all "
        "sensitive configuration. See Section 8.4 for secret management best practices.",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e


def section_installation(styles):
    e = []
    e.append(Paragraph("2. Installation", styles["h1"]))
    e.append(Paragraph(
        "This section covers the complete cluster installation process using kubeadm. "
        "Follow each step in order. Do not skip verification steps.",
        styles["body"],
    ))

    e.append(Paragraph("2.1 Cluster Bootstrap", styles["h2"]))
    e.append(Paragraph(
        "Initialize the control plane on the first master node. This process generates "
        "certificates, starts the API server, and creates the cluster configuration.",
        styles["body"],
    ))

    e.append(Paragraph("<b>Step 1:</b> Load required kernel modules on all nodes:", styles["numbered"]))
    e.append(code_block(
        "cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf\n"
        "overlay\n"
        "br_netfilter\n"
        "EOF\n"
        "\n"
        "sudo modprobe overlay\n"
        "sudo modprobe br_netfilter"
    ))

    e.append(Paragraph("<b>Step 2:</b> Configure sysctl parameters:", styles["numbered"]))
    e.append(code_block(
        "cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf\n"
        "net.bridge.bridge-nf-call-iptables  = 1\n"
        "net.bridge.bridge-nf-call-ip6tables = 1\n"
        "net.ipv4.ip_forward                 = 1\n"
        "EOF\n"
        "\n"
        "sudo sysctl --system"
    ))

    e.append(Paragraph("<b>Step 3:</b> Disable swap permanently:", styles["numbered"]))
    e.append(code_block(
        "sudo swapoff -a\n"
        "sudo sed -i '/swap/d' /etc/fstab\n"
        "\n"
        "# Verify swap is disabled\n"
        "free -h | grep -i swap\n"
        "# Should show: Swap: 0B 0B 0B"
    ))

    e.append(Paragraph("<b>Step 4:</b> Install Kubernetes packages:", styles["numbered"]))
    e.append(code_block(
        "# Add Kubernetes apt repository\n"
        "curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | \\\n"
        "  sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg\n"
        "\n"
        "echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \\\n"
        "  https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | \\\n"
        "  sudo tee /etc/apt/sources.list.d/kubernetes.list\n"
        "\n"
        "sudo apt-get update\n"
        "sudo apt-get install -y kubelet=1.30.2-1.1 kubeadm=1.30.2-1.1 kubectl=1.30.2-1.1\n"
        "sudo apt-mark hold kubelet kubeadm kubectl"
    ))

    e.append(Paragraph(
        "<b>NOTE:</b> Pin the package versions with apt-mark hold to prevent "
        "accidental upgrades during system updates. Kubernetes version skew policy "
        "only allows +/-1 minor version difference between components.",
        styles["note"],
    ))

    e.append(Paragraph("2.2 Control Plane Setup", styles["h2"]))
    e.append(Paragraph(
        "Initialize the first control plane node. The kubeadm init command performs "
        "preflight checks, generates PKI certificates, starts static pods, and "
        "bootstraps the cluster.",
        styles["body"],
    ))

    e.append(Paragraph("<b>Step 1:</b> Initialize the control plane:", styles["numbered"]))
    e.append(code_block(
        "sudo kubeadm init \\\n"
        "  --control-plane-endpoint=\"k8s-api.internal.example.com:6443\" \\\n"
        "  --upload-certs \\\n"
        "  --pod-network-cidr=10.244.0.0/16 \\\n"
        "  --service-cidr=10.96.0.0/12 \\\n"
        "  --kubernetes-version=v1.30.2 \\\n"
        "  --cri-socket=unix:///run/containerd/containerd.sock"
    ))

    e.append(Paragraph("<b>Step 2:</b> Configure kubectl access:", styles["numbered"]))
    e.append(code_block(
        "mkdir -p $HOME/.kube\n"
        "sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config\n"
        "sudo chown $(id -u):$(id -g) $HOME/.kube/config\n"
        "\n"
        "# Verify the API server is responding\n"
        "kubectl cluster-info\n"
        "kubectl get nodes"
    ))

    e.append(Paragraph("<b>Step 3:</b> Install the CNI plugin (Calico):", styles["numbered"]))
    e.append(code_block(
        "# Install Calico operator\n"
        "kubectl create -f https://raw.githubusercontent.com/projectcalico/\\\n"
        "  calico/v3.28.0/manifests/tigera-operator.yaml\n"
        "\n"
        "# Install Calico custom resources\n"
        "kubectl create -f https://raw.githubusercontent.com/projectcalico/\\\n"
        "  calico/v3.28.0/manifests/custom-resources.yaml\n"
        "\n"
        "# Wait for Calico pods\n"
        "kubectl wait --for=condition=Ready pods -l k8s-app=calico-node \\\n"
        "  -n calico-system --timeout=300s"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Do not install multiple CNI plugins. If migrating from "
        "Flannel to Calico, drain all nodes and fully remove Flannel resources first. "
        "Conflicting CNIs cause intermittent pod networking failures.",
        styles["warning"],
    ))

    e.append(Paragraph("2.3 Worker Node Join", styles["h2"]))
    e.append(Paragraph(
        "Join worker nodes to the cluster using the token generated during control "
        "plane initialization. Tokens expire after 24 hours.",
        styles["body"],
    ))

    e.append(Paragraph("<b>Step 1:</b> On the control plane, generate a join command:", styles["numbered"]))
    e.append(code_block(
        "# Generate new token if original expired\n"
        "kubeadm token create --print-join-command\n"
        "\n"
        "# Output will look like:\n"
        "# kubeadm join k8s-api.internal.example.com:6443 \\\n"
        "#   --token abcdef.0123456789abcdef \\\n"
        "#   --discovery-token-ca-cert-hash sha256:abc123..."
    ))

    e.append(Paragraph("<b>Step 2:</b> Run the join command on each worker node:", styles["numbered"]))
    e.append(code_block(
        "sudo kubeadm join k8s-api.internal.example.com:6443 \\\n"
        "  --token abcdef.0123456789abcdef \\\n"
        "  --discovery-token-ca-cert-hash sha256:abc123def456... \\\n"
        "  --cri-socket=unix:///run/containerd/containerd.sock"
    ))

    e.append(Paragraph("<b>Step 3:</b> Label worker nodes:", styles["numbered"]))
    e.append(code_block(
        "kubectl label node worker-1 node-role.kubernetes.io/worker=worker\n"
        "kubectl label node worker-2 node-role.kubernetes.io/worker=worker\n"
        "kubectl label node worker-3 node-role.kubernetes.io/worker=worker\n"
        "\n"
        "# Apply zone labels for topology-aware scheduling\n"
        "kubectl label node worker-1 topology.kubernetes.io/zone=us-east-1a\n"
        "kubectl label node worker-2 topology.kubernetes.io/zone=us-east-1b\n"
        "kubectl label node worker-3 topology.kubernetes.io/zone=us-east-1c"
    ))

    e.append(Paragraph("2.4 Verification", styles["h2"]))
    e.append(Paragraph(
        "After all nodes have joined, verify the cluster is healthy and all "
        "components are running:",
        styles["body"],
    ))
    e.append(code_block(
        "# Check all nodes are Ready\n"
        "kubectl get nodes -o wide\n"
        "\n"
        "# Expected output:\n"
        "# NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP\n"
        "# cp-1       Ready    control-plane   10m   v1.30.2   10.0.1.10\n"
        "# worker-1   Ready    worker          5m    v1.30.2   10.0.2.11\n"
        "# worker-2   Ready    worker          5m    v1.30.2   10.0.2.12\n"
        "# worker-3   Ready    worker          4m    v1.30.2   10.0.2.13\n"
        "\n"
        "# Check system pods\n"
        "kubectl get pods -n kube-system\n"
        "\n"
        "# Run a smoke test\n"
        "kubectl run nginx-test --image=nginx:1.27 --port=80\n"
        "kubectl expose pod nginx-test --type=NodePort --port=80\n"
        "kubectl get svc nginx-test\n"
        "curl http://worker-1:<nodeport>\n"
        "\n"
        "# Cleanup smoke test\n"
        "kubectl delete pod nginx-test\n"
        "kubectl delete svc nginx-test"
    ))

    e.append(Paragraph(
        "<b>NOTE:</b> If any node shows NotReady status, check kubelet logs with "
        "<font face='Courier'>journalctl -u kubelet -f</font>. Common causes include "
        "CNI not installed, containerd not running, or certificate issues. "
        "See Section 6.1 for detailed troubleshooting.",
        styles["note"],
    ))

    e.append(make_table([
        ["Check", "Command", "Expected Result"],
        ["API Server", "kubectl cluster-info", "Running at https://..."],
        ["Nodes Ready", "kubectl get nodes", "All STATUS = Ready"],
        ["System Pods", "kubectl get pods -n kube-system", "All Running/Completed"],
        ["DNS", "kubectl run -it dns-test --image=busybox -- nslookup kubernetes", "Resolves successfully"],
        ["Networking", "kubectl exec -it test -- ping <pod-ip>", "Replies received"],
    ], col_widths=[3*cm, 5*cm, 4.5*cm]))
    e.append(PageBreak())
    return e


def section_configuration(styles):
    e = []
    e.append(Paragraph("3. Configuration", styles["h1"]))
    e.append(Paragraph(
        "Post-installation configuration ensures the cluster meets operational "
        "requirements for networking, storage, resource management, and multi-tenancy.",
        styles["body"],
    ))

    e.append(Paragraph("3.1 Cluster Configuration", styles["h2"]))
    e.append(Paragraph(
        "The primary cluster configuration is managed through the kubeadm ConfigMap "
        "and various Kubernetes API objects. Key configurations include:",
        styles["body"],
    ))
    e.append(code_block(
        "# kubeadm-config ConfigMap\n"
        "apiVersion: kubeadm.k8s.io/v1beta3\n"
        "kind: ClusterConfiguration\n"
        "kubernetesVersion: v1.30.2\n"
        "controlPlaneEndpoint: \"k8s-api.internal.example.com:6443\"\n"
        "networking:\n"
        "  podSubnet: \"10.244.0.0/16\"\n"
        "  serviceSubnet: \"10.96.0.0/12\"\n"
        "  dnsDomain: \"cluster.local\"\n"
        "apiServer:\n"
        "  extraArgs:\n"
        "    audit-log-path: /var/log/kubernetes/audit.log\n"
        "    audit-log-maxage: \"30\"\n"
        "    audit-log-maxbackup: \"10\"\n"
        "    audit-log-maxsize: \"100\"\n"
        "    enable-admission-plugins: NodeRestriction,PodSecurity\n"
        "    encryption-provider-config: /etc/kubernetes/enc/encryption-config.yaml\n"
        "  extraVolumes:\n"
        "  - name: audit-log\n"
        "    hostPath: /var/log/kubernetes\n"
        "    mountPath: /var/log/kubernetes\n"
        "    pathType: DirectoryOrCreate"
    ))

    e.append(Paragraph(
        "Modify API server configuration carefully. Changes require API server restart. "
        "Always test in a non-production environment first.",
        styles["body"],
    ))

    e.append(Paragraph("3.2 Networking", styles["h2"]))
    e.append(Paragraph(
        "Configure advanced networking features including network policies, "
        "load balancer integration, and DNS customization.",
        styles["body"],
    ))
    e.append(Paragraph("CoreDNS Configuration:", styles["h3"]))
    e.append(code_block(
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: coredns\n"
        "  namespace: kube-system\n"
        "data:\n"
        "  Corefile: |\n"
        "    .:53 {\n"
        "        errors\n"
        "        health {\n"
        "          lameduck 5s\n"
        "        }\n"
        "        ready\n"
        "        kubernetes cluster.local in-addr.arpa ip6.arpa {\n"
        "          pods insecure\n"
        "          fallthrough in-addr.arpa ip6.arpa\n"
        "          ttl 30\n"
        "        }\n"
        "        prometheus :9153\n"
        "        forward . /etc/resolv.conf {\n"
        "          max_concurrent 1000\n"
        "        }\n"
        "        cache 30\n"
        "        loop\n"
        "        reload\n"
        "        loadbalance\n"
        "    }\n"
        "    internal.example.com:53 {\n"
        "        forward . 10.0.0.2 10.0.0.3\n"
        "    }"
    ))

    e.append(Paragraph("Environment variables for DNS configuration:", styles["body"]))
    e.append(make_table([
        ["Variable", "Default", "Description"],
        ["CLUSTER_DNS", "10.96.0.10", "ClusterIP of CoreDNS service"],
        ["CLUSTER_DOMAIN", "cluster.local", "Internal DNS domain suffix"],
        ["DNS_POLICY", "ClusterFirst", "Pod DNS resolution policy"],
        ["NDOTS", "5", "Threshold for absolute DNS names"],
    ], col_widths=[3.5*cm, 3.5*cm, 7.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph(
        "<b>NOTE:</b> High ndots values (default 5) cause excessive DNS lookups for "
        "external domains. For workloads making many external API calls, set "
        "<font face='Courier'>dnsConfig.options: [{name: ndots, value: \"2\"}]</font> "
        "in the pod spec. See Section 6.2 for DNS troubleshooting.",
        styles["note"],
    ))

    e.append(Paragraph("3.3 Storage Classes", styles["h2"]))
    e.append(Paragraph(
        "Define StorageClasses for different performance tiers. Each class maps to "
        "a specific backend provisioner.",
        styles["body"],
    ))
    e.append(code_block(
        "apiVersion: storage.k8s.io/v1\n"
        "kind: StorageClass\n"
        "metadata:\n"
        "  name: fast-ssd\n"
        "  annotations:\n"
        "    storageclass.kubernetes.io/is-default-class: \"false\"\n"
        "provisioner: ebs.csi.aws.com\n"
        "parameters:\n"
        "  type: gp3\n"
        "  iops: \"5000\"\n"
        "  throughput: \"250\"\n"
        "  encrypted: \"true\"\n"
        "  kmsKeyId: arn:aws:kms:us-east-1:123456789:key/abc-def-ghi\n"
        "reclaimPolicy: Retain\n"
        "allowVolumeExpansion: true\n"
        "volumeBindingMode: WaitForFirstConsumer\n"
        "---\n"
        "apiVersion: storage.k8s.io/v1\n"
        "kind: StorageClass\n"
        "metadata:\n"
        "  name: standard\n"
        "  annotations:\n"
        "    storageclass.kubernetes.io/is-default-class: \"true\"\n"
        "provisioner: ebs.csi.aws.com\n"
        "parameters:\n"
        "  type: gp3\n"
        "  encrypted: \"true\"\n"
        "reclaimPolicy: Delete\n"
        "allowVolumeExpansion: true\n"
        "volumeBindingMode: WaitForFirstConsumer"
    ))

    e.append(make_table([
        ["Storage Class", "Provisioner", "IOPS", "Use Case"],
        ["fast-ssd", "ebs.csi.aws.com (gp3)", "5000", "Databases, etcd"],
        ["standard", "ebs.csi.aws.com (gp3)", "3000 (default)", "General workloads"],
        ["cold-storage", "ebs.csi.aws.com (sc1)", "250", "Archival, logs"],
        ["local-nvme", "kubernetes.io/no-provisioner", "N/A", "Performance-critical"],
    ], col_widths=[3*cm, 4.5*cm, 2.5*cm, 4.5*cm]))

    e.append(Paragraph("3.4 Resource Quotas", styles["h2"]))
    e.append(Paragraph(
        "Resource quotas prevent any single namespace from consuming excessive "
        "cluster resources. Apply quotas to all tenant namespaces.",
        styles["body"],
    ))
    e.append(code_block(
        "apiVersion: v1\n"
        "kind: ResourceQuota\n"
        "metadata:\n"
        "  name: team-alpha-quota\n"
        "  namespace: team-alpha\n"
        "spec:\n"
        "  hard:\n"
        "    requests.cpu: \"20\"\n"
        "    requests.memory: 64Gi\n"
        "    limits.cpu: \"40\"\n"
        "    limits.memory: 128Gi\n"
        "    persistentvolumeclaims: \"20\"\n"
        "    pods: \"100\"\n"
        "    services: \"30\"\n"
        "    services.loadbalancers: \"5\"\n"
        "---\n"
        "apiVersion: v1\n"
        "kind: LimitRange\n"
        "metadata:\n"
        "  name: team-alpha-limits\n"
        "  namespace: team-alpha\n"
        "spec:\n"
        "  limits:\n"
        "  - default:\n"
        "      cpu: 500m\n"
        "      memory: 512Mi\n"
        "    defaultRequest:\n"
        "      cpu: 100m\n"
        "      memory: 128Mi\n"
        "    max:\n"
        "      cpu: \"4\"\n"
        "      memory: 8Gi\n"
        "    min:\n"
        "      cpu: 50m\n"
        "      memory: 64Mi\n"
        "    type: Container"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Without LimitRange defaults, pods without resource requests "
        "will be scheduled without limits, potentially causing node resource exhaustion. "
        "Always pair ResourceQuota with LimitRange in every namespace.",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e


def section_deployments(styles):
    e = []
    e.append(Paragraph("4. Deployments & Services", styles["h1"]))
    e.append(Paragraph(
        "This section covers deployment strategies, service exposure patterns, "
        "ingress configuration, and Helm-based application management.",
        styles["body"],
    ))

    e.append(Paragraph("4.1 Deployment Strategies", styles["h2"]))
    e.append(Paragraph(
        "Kubernetes supports multiple deployment strategies. Choose based on your "
        "application's tolerance for downtime and risk appetite.",
        styles["body"],
    ))
    e.append(make_table([
        ["Strategy", "Downtime", "Rollback Speed", "Resource Cost", "Use Case"],
        ["RollingUpdate", "Zero", "Fast (automatic)", "1.25x-2x", "Stateless apps"],
        ["Recreate", "Brief", "Manual", "1x", "Stateful, single-instance"],
        ["Blue/Green", "Zero", "Instant (swap)", "2x", "Critical services"],
        ["Canary", "Zero", "Instant (route)", "1.1x", "High-risk changes"],
    ], col_widths=[2.5*cm, 2*cm, 3*cm, 2.5*cm, 3.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Rolling Update Deployment:", styles["h3"]))
    e.append(code_block(
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: api-server\n"
        "  namespace: production\n"
        "  labels:\n"
        "    app: api-server\n"
        "    version: v2.3.1\n"
        "spec:\n"
        "  replicas: 5\n"
        "  strategy:\n"
        "    type: RollingUpdate\n"
        "    rollingUpdate:\n"
        "      maxSurge: 1\n"
        "      maxUnavailable: 0\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: api-server\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: api-server\n"
        "        version: v2.3.1\n"
        "    spec:\n"
        "      containers:\n"
        "      - name: api\n"
        "        image: registry.example.com/api-server:v2.3.1\n"
        "        ports:\n"
        "        - containerPort: 8080\n"
        "        resources:\n"
        "          requests:\n"
        "            cpu: 250m\n"
        "            memory: 512Mi\n"
        "          limits:\n"
        "            cpu: \"1\"\n"
        "            memory: 1Gi\n"
        "        readinessProbe:\n"
        "          httpGet:\n"
        "            path: /healthz\n"
        "            port: 8080\n"
        "          initialDelaySeconds: 5\n"
        "          periodSeconds: 10\n"
        "        livenessProbe:\n"
        "          httpGet:\n"
        "            path: /healthz\n"
        "            port: 8080\n"
        "          initialDelaySeconds: 30\n"
        "          periodSeconds: 30\n"
        "          failureThreshold: 3"
    ))

    e.append(Paragraph(
        "Deploy and monitor the rollout:",
        styles["body"],
    ))
    e.append(code_block(
        "# Apply the deployment\n"
        "kubectl apply -f deploy-api-server.yaml\n"
        "\n"
        "# Monitor rollout status\n"
        "kubectl rollout status deployment/api-server -n production\n"
        "\n"
        "# Watch pods transition\n"
        "kubectl get pods -n production -l app=api-server -w\n"
        "\n"
        "# If issues detected, rollback immediately\n"
        "kubectl rollout undo deployment/api-server -n production\n"
        "\n"
        "# View rollout history\n"
        "kubectl rollout history deployment/api-server -n production"
    ))

    e.append(Paragraph("4.2 Service Types", styles["h2"]))
    e.append(Paragraph(
        "Services provide stable network endpoints for pods. Choose the type based "
        "on how the service needs to be accessed.",
        styles["body"],
    ))
    e.append(make_table([
        ["Service Type", "Scope", "Load Balancer", "Use Case"],
        ["ClusterIP", "Internal only", "kube-proxy", "Inter-service communication"],
        ["NodePort", "External (node IP)", "kube-proxy", "Development, debugging"],
        ["LoadBalancer", "External (cloud LB)", "Cloud provider", "Production traffic"],
        ["ExternalName", "DNS alias", "None (CNAME)", "External service reference"],
    ], col_widths=[3*cm, 3.5*cm, 3*cm, 5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(code_block(
        "apiVersion: v1\n"
        "kind: Service\n"
        "metadata:\n"
        "  name: api-server\n"
        "  namespace: production\n"
        "  annotations:\n"
        "    service.beta.kubernetes.io/aws-load-balancer-type: nlb\n"
        "    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing\n"
        "    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: \"true\"\n"
        "spec:\n"
        "  type: LoadBalancer\n"
        "  selector:\n"
        "    app: api-server\n"
        "  ports:\n"
        "  - name: http\n"
        "    port: 80\n"
        "    targetPort: 8080\n"
        "    protocol: TCP\n"
        "  - name: https\n"
        "    port: 443\n"
        "    targetPort: 8443\n"
        "    protocol: TCP"
    ))

    e.append(Paragraph("4.3 Ingress Configuration", styles["h2"]))
    e.append(Paragraph(
        "Ingress provides HTTP/HTTPS routing with TLS termination, path-based "
        "routing, and virtual host support. We use nginx-ingress-controller.",
        styles["body"],
    ))
    e.append(code_block(
        "# Install nginx ingress controller via Helm\n"
        "helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx\n"
        "helm repo update\n"
        "\n"
        "helm install ingress-nginx ingress-nginx/ingress-nginx \\\n"
        "  --namespace ingress-system \\\n"
        "  --create-namespace \\\n"
        "  --set controller.replicaCount=3 \\\n"
        "  --set controller.resources.requests.cpu=100m \\\n"
        "  --set controller.resources.requests.memory=256Mi \\\n"
        "  --set controller.metrics.enabled=true \\\n"
        "  --set controller.podAnnotations.\"prometheus\\.io/scrape\"=true"
    ))

    e.append(Paragraph("Ingress resource with TLS and path-based routing:", styles["body"]))
    e.append(code_block(
        "apiVersion: networking.k8s.io/v1\n"
        "kind: Ingress\n"
        "metadata:\n"
        "  name: main-ingress\n"
        "  namespace: production\n"
        "  annotations:\n"
        "    nginx.ingress.kubernetes.io/ssl-redirect: \"true\"\n"
        "    nginx.ingress.kubernetes.io/proxy-body-size: \"50m\"\n"
        "    cert-manager.io/cluster-issuer: letsencrypt-prod\n"
        "spec:\n"
        "  ingressClassName: nginx\n"
        "  tls:\n"
        "  - hosts:\n"
        "    - api.example.com\n"
        "    - app.example.com\n"
        "    secretName: tls-example-com\n"
        "  rules:\n"
        "  - host: api.example.com\n"
        "    http:\n"
        "      paths:\n"
        "      - path: /v1\n"
        "        pathType: Prefix\n"
        "        backend:\n"
        "          service:\n"
        "            name: api-server\n"
        "            port:\n"
        "              number: 80\n"
        "  - host: app.example.com\n"
        "    http:\n"
        "      paths:\n"
        "      - path: /\n"
        "        pathType: Prefix\n"
        "        backend:\n"
        "          service:\n"
        "            name: frontend\n"
        "            port:\n"
        "              number: 80"
    ))

    e.append(Paragraph("4.4 Helm Charts", styles["h2"]))
    e.append(Paragraph(
        "Helm simplifies application deployment with templated manifests and release "
        "management. Use Helm for all production deployments.",
        styles["body"],
    ))
    e.append(code_block(
        "# Create a new chart\n"
        "helm create myapp\n"
        "\n"
        "# Install a release\n"
        "helm install myapp-prod ./myapp \\\n"
        "  --namespace production \\\n"
        "  --values values-prod.yaml \\\n"
        "  --set image.tag=v2.3.1 \\\n"
        "  --wait --timeout 5m\n"
        "\n"
        "# Upgrade an existing release\n"
        "helm upgrade myapp-prod ./myapp \\\n"
        "  --namespace production \\\n"
        "  --values values-prod.yaml \\\n"
        "  --set image.tag=v2.4.0 \\\n"
        "  --wait --timeout 5m\n"
        "\n"
        "# Rollback to previous release\n"
        "helm rollback myapp-prod 1 --namespace production\n"
        "\n"
        "# List releases\n"
        "helm list -n production"
    ))

    e.append(Paragraph(
        "<b>NOTE:</b> Always use <font face='Courier'>--wait</font> flag in CI/CD "
        "pipelines to ensure Helm waits for all resources to become ready. Without it, "
        "the pipeline may report success while pods are still starting or crashing. "
        "See Section 6.1 for diagnosing Helm deployment failures.",
        styles["note"],
    ))
    e.append(PageBreak())
    return e


def section_monitoring(styles):
    e = []
    e.append(Paragraph("5. Monitoring & Observability", styles["h1"]))
    e.append(Paragraph(
        "A comprehensive monitoring stack is essential for maintaining cluster health. "
        "This section covers Prometheus, Grafana, alerting, and log aggregation.",
        styles["body"],
    ))

    e.append(Paragraph("5.1 Prometheus Setup", styles["h2"]))
    e.append(Paragraph(
        "Deploy Prometheus using the kube-prometheus-stack Helm chart. This includes "
        "Prometheus Operator, Alertmanager, Grafana, and default recording rules.",
        styles["body"],
    ))
    e.append(code_block(
        "# Add Prometheus community Helm repo\n"
        "helm repo add prometheus-community \\\n"
        "  https://prometheus-community.github.io/helm-charts\n"
        "helm repo update\n"
        "\n"
        "# Install kube-prometheus-stack\n"
        "helm install monitoring prometheus-community/kube-prometheus-stack \\\n"
        "  --namespace monitoring \\\n"
        "  --create-namespace \\\n"
        "  --set prometheus.prometheusSpec.retention=30d \\\n"
        "  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi \\\n"
        "  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=fast-ssd \\\n"
        "  --set grafana.persistence.enabled=true \\\n"
        "  --set grafana.persistence.size=10Gi \\\n"
        "  --values prometheus-values.yaml"
    ))

    e.append(Paragraph("Key metrics to monitor:", styles["body"]))
    e.append(make_table([
        ["Metric", "Type", "Description", "Alert Threshold"],
        ["node_cpu_seconds_total", "Counter", "CPU time per mode", ">85% sustained"],
        ["node_memory_MemAvailable_bytes", "Gauge", "Available memory", "<10% of total"],
        ["kubelet_running_pods", "Gauge", "Running pods per node", ">110 (default max)"],
        ["kube_pod_status_phase", "Gauge", "Pod phase (Pending/Running)", "Pending >5min"],
        ["container_memory_working_set_bytes", "Gauge", "Container memory usage", ">90% of limit"],
    ], col_widths=[4.5*cm, 2*cm, 4*cm, 3.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Custom ServiceMonitor for application metrics:", styles["body"]))
    e.append(code_block(
        "apiVersion: monitoring.coreos.com/v1\n"
        "kind: ServiceMonitor\n"
        "metadata:\n"
        "  name: api-server-metrics\n"
        "  namespace: monitoring\n"
        "  labels:\n"
        "    release: monitoring\n"
        "spec:\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: api-server\n"
        "  namespaceSelector:\n"
        "    matchNames:\n"
        "    - production\n"
        "  endpoints:\n"
        "  - port: metrics\n"
        "    interval: 30s\n"
        "    path: /metrics\n"
        "    scrapeTimeout: 10s"
    ))

    e.append(Paragraph("5.2 Grafana Dashboards", styles["h2"]))
    e.append(Paragraph(
        "Import the following dashboards for cluster visibility. These are available "
        "from grafana.com or can be created from the JSON definitions below.",
        styles["body"],
    ))
    e.append(make_table([
        ["Dashboard", "ID", "Purpose"],
        ["Kubernetes Cluster Overview", "6417", "Overall cluster health and resource usage"],
        ["Node Exporter Full", "1860", "Detailed node-level metrics"],
        ["Kubernetes Pods", "6336", "Pod-level resource consumption"],
        ["CoreDNS", "5926", "DNS query rates, errors, latency"],
        ["NGINX Ingress", "9614", "Request rates, latency, error rates"],
    ], col_widths=[5*cm, 2*cm, 7.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Provisioning dashboards via ConfigMap:", styles["body"]))
    e.append(code_block(
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: grafana-dashboards\n"
        "  namespace: monitoring\n"
        "  labels:\n"
        "    grafana_dashboard: \"1\"\n"
        "data:\n"
        "  cluster-overview.json: |\n"
        "    {\n"
        "      \"dashboard\": {\n"
        "        \"title\": \"Cluster Overview\",\n"
        "        \"panels\": [\n"
        "          {\n"
        "            \"title\": \"CPU Usage by Node\",\n"
        "            \"type\": \"timeseries\",\n"
        "            \"targets\": [{\n"
        "              \"expr\": \"100 - (avg by(instance)(irate(node_cpu_seconds_total{mode=\\\"idle\\\"}[5m])) * 100)\"\n"
        "            }]\n"
        "          }\n"
        "        ]\n"
        "      }\n"
        "    }"
    ))

    e.append(Paragraph("5.3 Alert Rules", styles["h2"]))
    e.append(Paragraph(
        "Define PrometheusRule resources for critical alerts. These rules are "
        "automatically loaded by the Prometheus Operator.",
        styles["body"],
    ))
    e.append(code_block(
        "apiVersion: monitoring.coreos.com/v1\n"
        "kind: PrometheusRule\n"
        "metadata:\n"
        "  name: cluster-critical-alerts\n"
        "  namespace: monitoring\n"
        "  labels:\n"
        "    release: monitoring\n"
        "spec:\n"
        "  groups:\n"
        "  - name: cluster.rules\n"
        "    rules:\n"
        "    - alert: NodeNotReady\n"
        "      expr: kube_node_status_condition{condition=\"Ready\",status=\"true\"} == 0\n"
        "      for: 5m\n"
        "      labels:\n"
        "        severity: critical\n"
        "      annotations:\n"
        "        summary: \"Node {{ $labels.node }} is not ready\"\n"
        "        description: \"Node has been in NotReady state for more than 5 minutes\"\n"
        "    - alert: PodCrashLooping\n"
        "      expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 5 > 0\n"
        "      for: 15m\n"
        "      labels:\n"
        "        severity: warning\n"
        "      annotations:\n"
        "        summary: \"Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping\"\n"
        "    - alert: HighMemoryPressure\n"
        "      expr: |\n"
        "        container_memory_working_set_bytes{container!=\"\"}\n"
        "        / container_spec_memory_limit_bytes{container!=\"\"} > 0.9\n"
        "      for: 5m\n"
        "      labels:\n"
        "        severity: warning\n"
        "      annotations:\n"
        "        summary: \"Container {{ $labels.container }} in pod {{ $labels.pod }} using >90% memory\""
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Ensure all critical alerts have a <font face='Courier'>for</font> "
        "duration to avoid alert fatigue from transient spikes. Set severity labels correctly "
        "as they route to different notification channels in Alertmanager.",
        styles["warning"],
    ))

    e.append(Paragraph("5.4 Log Aggregation", styles["h2"]))
    e.append(Paragraph(
        "Deploy a centralized logging stack using Fluent Bit for collection and "
        "OpenSearch for storage and search. Fluent Bit runs as a DaemonSet on all nodes.",
        styles["body"],
    ))
    e.append(code_block(
        "# Install Fluent Bit via Helm\n"
        "helm repo add fluent https://fluent.github.io/helm-charts\n"
        "helm install fluent-bit fluent/fluent-bit \\\n"
        "  --namespace logging \\\n"
        "  --create-namespace \\\n"
        "  --set config.outputs=\"\"\"\n"
        "[OUTPUT]\n"
        "    Name            opensearch\n"
        "    Match           kube.*\n"
        "    Host            opensearch.logging.svc.cluster.local\n"
        "    Port            9200\n"
        "    Index           k8s-logs\n"
        "    Type            _doc\n"
        "    Suppress_Type_Name On\n"
        "    tls             On\n"
        "    tls.verify      Off\n"
        "\"\"\""
    ))

    for item in [
        "Retain logs for 30 days in hot storage, 90 days in warm storage",
        "Index lifecycle policies should move indices from hot to warm after 7 days",
        "Use namespace-based index patterns for access control",
        "Configure log rotation on nodes to prevent disk pressure (see Section 6.3)",
        "Set resource limits on Fluent Bit DaemonSet to prevent OOM on log-heavy nodes",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>NOTE:</b> For high-volume environments (>10GB logs/day), consider using "
        "Kafka as a buffer between Fluent Bit and OpenSearch to handle backpressure "
        "during OpenSearch maintenance windows.",
        styles["note"],
    ))
    e.append(PageBreak())
    return e


def section_troubleshooting(styles):
    e = []
    e.append(Paragraph("6. Troubleshooting", styles["h1"]))
    e.append(Paragraph(
        "This section provides structured approaches to diagnosing and resolving "
        "common Kubernetes operational issues. Follow the problem/cause/solution format.",
        styles["body"],
    ))

    e.append(Paragraph("6.1 Pod Failures", styles["h2"]))
    e.append(Paragraph("Problem: Pod stuck in CrashLoopBackOff", styles["h3"]))
    e.append(Paragraph(
        "<b>Symptoms:</b> Pod restarts repeatedly. STATUS shows CrashLoopBackOff with "
        "increasing backoff delay (10s, 20s, 40s, ... up to 5 minutes).",
        styles["body"],
    ))
    e.append(Paragraph("<b>Diagnostic Steps:</b>", styles["body"]))
    e.append(code_block(
        "# Check pod events\n"
        "kubectl describe pod <pod-name> -n <namespace>\n"
        "\n"
        "# Check container logs (current crash)\n"
        "kubectl logs <pod-name> -n <namespace> --previous\n"
        "\n"
        "# Check exit code\n"
        "kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'\n"
        "\n"
        "# Common exit codes:\n"
        "# 1   - Application error (check app logs)\n"
        "# 137 - OOMKilled (container exceeded memory limit)\n"
        "# 139 - Segfault (binary compatibility issue)\n"
        "# 143 - SIGTERM (graceful shutdown timeout exceeded)"
    ))

    e.append(Paragraph("<b>Common Causes and Solutions:</b>", styles["body"]))
    e.append(make_table([
        ["Cause", "Indicator", "Solution"],
        ["OOM Killed", "Exit code 137, OOMKilled reason", "Increase memory limits or fix leak"],
        ["Config error", "Exit code 1, error in logs", "Check ConfigMap/Secret mounts"],
        ["Missing dependency", "Connection refused in logs", "Verify dependent services exist"],
        ["Image pull failure", "ErrImagePull event", "Check registry credentials, image tag"],
        ["Readiness probe", "Probe failing in events", "Adjust initialDelaySeconds, thresholds"],
    ], col_widths=[3*cm, 4.5*cm, 6*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Problem: Pod stuck in Pending state", styles["h3"]))
    e.append(Paragraph(
        "<b>Symptoms:</b> Pod remains in Pending state. No container ever starts.",
        styles["body"],
    ))
    e.append(code_block(
        "# Check why pod is pending\n"
        "kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Events\n"
        "\n"
        "# Check node resources\n"
        "kubectl top nodes\n"
        "kubectl describe nodes | grep -A 5 \"Allocated resources\"\n"
        "\n"
        "# Check for taints blocking scheduling\n"
        "kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints\n"
        "\n"
        "# Example output showing insufficient resources:\n"
        "# Events:\n"
        "#   Warning  FailedScheduling  default-scheduler\n"
        "#   0/3 nodes are available: 3 Insufficient memory."
    ))

    e.append(Paragraph(
        "<b>NOTE:</b> If cluster-autoscaler is configured, Pending pods due to "
        "insufficient resources should trigger scale-up within 30-60 seconds. "
        "If not scaling, check autoscaler logs: "
        "<font face='Courier'>kubectl logs -n kube-system -l app=cluster-autoscaler</font>",
        styles["note"],
    ))

    e.append(Paragraph("6.2 Network Issues", styles["h2"]))
    e.append(Paragraph("Problem: DNS resolution failing inside pods", styles["h3"]))
    e.append(Paragraph(
        "<b>Symptoms:</b> Applications report connection timeouts to other services. "
        "nslookup fails from within pods.",
        styles["body"],
    ))
    e.append(code_block(
        "# Test DNS from a debug pod\n"
        "kubectl run -it dns-debug --image=nicolaka/netshoot -- bash\n"
        "\n"
        "# Inside the pod:\n"
        "nslookup kubernetes.default.svc.cluster.local\n"
        "nslookup api-server.production.svc.cluster.local\n"
        "cat /etc/resolv.conf\n"
        "\n"
        "# Check CoreDNS pod status\n"
        "kubectl get pods -n kube-system -l k8s-app=kube-dns\n"
        "kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50\n"
        "\n"
        "# Check CoreDNS metrics\n"
        "kubectl exec -n kube-system -it <coredns-pod> -- \\\n"
        "  wget -qO- http://localhost:9153/metrics | grep coredns_dns_requests_total"
    ))

    e.append(Paragraph("Problem: Service-to-service connectivity failure", styles["h3"]))
    e.append(code_block(
        "# Verify service has endpoints\n"
        "kubectl get endpoints <service-name> -n <namespace>\n"
        "\n"
        "# If endpoints are empty, check selector matches pod labels:\n"
        "kubectl get svc <service-name> -n <namespace> -o yaml | grep -A 3 selector\n"
        "kubectl get pods -n <namespace> --show-labels | grep <app-label>\n"
        "\n"
        "# Test connectivity from within cluster\n"
        "kubectl run -it nettest --image=nicolaka/netshoot -- bash\n"
        "curl -v http://<service-name>.<namespace>.svc.cluster.local:<port>/healthz\n"
        "\n"
        "# Check network policies blocking traffic\n"
        "kubectl get networkpolicies -n <namespace>\n"
        "kubectl describe networkpolicy <policy-name> -n <namespace>"
    ))

    e.append(Paragraph("6.3 Storage Problems", styles["h2"]))
    e.append(Paragraph("Problem: PVC stuck in Pending state", styles["h3"]))
    e.append(code_block(
        "# Check PVC status and events\n"
        "kubectl describe pvc <pvc-name> -n <namespace>\n"
        "\n"
        "# Common causes:\n"
        "# 1. StorageClass not found\n"
        "kubectl get storageclass\n"
        "\n"
        "# 2. No available PVs (for static provisioning)\n"
        "kubectl get pv\n"
        "\n"
        "# 3. CSI driver not installed\n"
        "kubectl get csidrivers\n"
        "kubectl get pods -n kube-system -l app=ebs-csi-controller\n"
        "\n"
        "# 4. Zone mismatch (WaitForFirstConsumer)\n"
        "kubectl get pvc <pvc-name> -o yaml | grep volumeBindingMode"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Never delete a PVC that is bound to a PV with "
        "<font face='Courier'>reclaimPolicy: Delete</font> unless you have confirmed "
        "the data is backed up. Deletion will destroy the underlying storage volume "
        "permanently. See Section 7.2 for backup procedures.",
        styles["warning"],
    ))

    e.append(Paragraph("6.4 Performance Degradation", styles["h2"]))
    e.append(Paragraph(
        "When cluster performance degrades, follow this diagnostic sequence:",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Check node resource utilization:", styles["numbered"]))
    e.append(code_block(
        "kubectl top nodes\n"
        "kubectl top pods -n <namespace> --sort-by=cpu\n"
        "kubectl top pods -n <namespace> --sort-by=memory"
    ))
    e.append(Paragraph("<b>Step 2:</b> Check for throttled containers:", styles["numbered"]))
    e.append(code_block(
        "# Query Prometheus for CPU throttling\n"
        "# rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0\n"
        "\n"
        "# Check container resource limits vs actual usage\n"
        "kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{\"\\t\"}{.spec.containers[*].resources}{\"\\n\"}{end}'"
    ))
    e.append(Paragraph("<b>Step 3:</b> Check API server latency:", styles["numbered"]))
    e.append(code_block(
        "# Query: histogram_quantile(0.99,\n"
        "#   rate(apiserver_request_duration_seconds_bucket[5m]))\n"
        "\n"
        "# Check for slow API requests\n"
        "kubectl get --raw /metrics | grep apiserver_request_duration"
    ))
    e.append(Paragraph(
        "<b>NOTE:</b> API server latency above 1 second for non-LIST operations "
        "indicates etcd performance issues. Check etcd disk IOPS and network "
        "latency between etcd members. Cross-reference with Section 5.1 metrics.",
        styles["note"],
    ))

    e.append(Paragraph("6.5 Common Error Messages Reference", styles["h2"]))
    e.append(Paragraph(
        "Quick lookup table for frequently encountered error messages in Kubernetes "
        "logs and events. Each entry includes the source, meaning, and resolution.",
        styles["body"],
    ))
    e.append(make_table([
        ["Error Message", "Source", "Resolution"],
        ["Back-off restarting failed container", "kubelet", "Check logs --previous, fix app crash"],
        ["nodes are available: Insufficient cpu", "scheduler", "Scale cluster or reduce requests"],
        ["dial tcp: lookup X: no such host", "Pod DNS", "Check CoreDNS, network policies"],
        ["connection refused", "Any client", "Target pod not ready or port wrong"],
        ["context deadline exceeded", "API client", "Network partition or server overload"],
    ], col_widths=[5*cm, 2.5*cm, 6*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Example: Interpreting kubelet log output", styles["h3"]))
    e.append(code_block(
        "# Typical kubelet log showing eviction sequence:\n"
        "Jun 17 08:23:41 worker-2 kubelet[1432]: I0617 08:23:41.123456 eviction_manager.go:344]\n"
        "  \"Eviction manager: must evict pod(s) to reclaim\" resource=\"ephemeral-storage\"\n"
        "Jun 17 08:23:41 worker-2 kubelet[1432]: I0617 08:23:41.123789 eviction_manager.go:362]\n"
        "  \"Eviction manager: pods ranked for eviction\" pods=[\"logging/fluent-bit-abc12\"]\n"
        "Jun 17 08:23:41 worker-2 kubelet[1432]: I0617 08:23:41.124001 eviction_manager.go:380]\n"
        "  \"Eviction manager: evicting pod\" pod=\"logging/fluent-bit-abc12\"\n"
        "\n"
        "# Interpreting the sequence:\n"
        "# 1. Node hit ephemeral-storage threshold (default: 85%)\n"
        "# 2. Kubelet ranked pods by priority and resource usage\n"
        "# 3. Lowest priority pod evicted first\n"
        "# Resolution: Increase node disk, set resource limits, enable log rotation"
    ))

    e.append(Paragraph("Example: API server audit log for debugging RBAC denials", styles["h3"]))
    e.append(code_block(
        "# Search audit log for forbidden requests\n"
        "grep '\"code\":403' /var/log/kubernetes/audit.log | jq '{\n"
        "  user: .user.username,\n"
        "  verb: .verb,\n"
        "  resource: .objectRef.resource,\n"
        "  namespace: .objectRef.namespace,\n"
        "  timestamp: .requestReceivedTimestamp\n"
        "}' | head -20\n"
        "\n"
        "# Example output:\n"
        "# {\n"
        "#   \"user\": \"developer@example.com\",\n"
        "#   \"verb\": \"delete\",\n"
        "#   \"resource\": \"deployments\",\n"
        "#   \"namespace\": \"production\",\n"
        "#   \"timestamp\": \"2026-06-17T15:23:41.000000Z\"\n"
        "# }\n"
        "\n"
        "# Fix: Add 'delete' verb to the developer Role for deployments\n"
        "# See Section 8.1 for RBAC configuration"
    ))

    e.append(Paragraph("Example: Container runtime (containerd) debugging", styles["h3"]))
    e.append(code_block(
        "# Check containerd status\n"
        "sudo systemctl status containerd\n"
        "sudo journalctl -u containerd --since '5 minutes ago'\n"
        "\n"
        "# List running containers\n"
        "sudo crictl ps\n"
        "sudo crictl ps -a  # Include stopped containers\n"
        "\n"
        "# Inspect a specific container\n"
        "sudo crictl inspect <container-id>\n"
        "\n"
        "# Check image pull issues\n"
        "sudo crictl pull <image-name>\n"
        "sudo crictl images\n"
        "\n"
        "# Clean up unused images (when disk pressure)\n"
        "sudo crictl rmi --prune\n"
        "\n"
        "# Common containerd errors:\n"
        "# 'failed to pull image': Registry unreachable or auth failed\n"
        "# 'failed to create containerd task': OOM or cgroup issue\n"
        "# 'context canceled': Timeout during image pull (large image)"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Running <font face='Courier'>crictl rmi --prune</font> removes "
        "all images not referenced by running containers. In environments with frequent "
        "rollbacks, this may force re-pulling of previous deployment images. Use with "
        "caution during active incidents.",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e


def section_backup(styles):
    e = []
    e.append(Paragraph("7. Backup & Recovery", styles["h1"]))
    e.append(Paragraph(
        "Regular backups are essential for disaster recovery. This section covers "
        "etcd backup, persistent volume snapshots, and complete cluster recovery procedures.",
        styles["body"],
    ))

    e.append(Paragraph("7.1 etcd Backup", styles["h2"]))
    e.append(Paragraph(
        "etcd stores all cluster state including workload definitions, ConfigMaps, "
        "Secrets, and RBAC policies. Without etcd backups, a complete cluster "
        "rebuild from scratch is required after data loss.",
        styles["body"],
    ))

    e.append(Paragraph("<b>Step 1:</b> Create a manual etcd snapshot:", styles["numbered"]))
    e.append(code_block(
        "# Set environment variables\n"
        "export ETCDCTL_API=3\n"
        "export ETCD_ENDPOINTS=https://127.0.0.1:2379\n"
        "export ETCD_CACERT=/etc/kubernetes/pki/etcd/ca.crt\n"
        "export ETCD_CERT=/etc/kubernetes/pki/etcd/server.crt\n"
        "export ETCD_KEY=/etc/kubernetes/pki/etcd/server.key\n"
        "\n"
        "# Take snapshot\n"
        "etcdctl snapshot save /backup/etcd-snapshot-$(date +%Y%m%d-%H%M%S).db \\\n"
        "  --endpoints=$ETCD_ENDPOINTS \\\n"
        "  --cacert=$ETCD_CACERT \\\n"
        "  --cert=$ETCD_CERT \\\n"
        "  --key=$ETCD_KEY\n"
        "\n"
        "# Verify snapshot\n"
        "etcdctl snapshot status /backup/etcd-snapshot-*.db --write-table"
    ))

    e.append(Paragraph("<b>Step 2:</b> Automate with a CronJob:", styles["numbered"]))
    e.append(code_block(
        "apiVersion: batch/v1\n"
        "kind: CronJob\n"
        "metadata:\n"
        "  name: etcd-backup\n"
        "  namespace: kube-system\n"
        "spec:\n"
        "  schedule: \"0 */6 * * *\"  # Every 6 hours\n"
        "  concurrencyPolicy: Forbid\n"
        "  successfulJobsHistoryLimit: 3\n"
        "  failedJobsHistoryLimit: 3\n"
        "  jobTemplate:\n"
        "    spec:\n"
        "      template:\n"
        "        spec:\n"
        "          hostNetwork: true\n"
        "          nodeSelector:\n"
        "            node-role.kubernetes.io/control-plane: \"\"\n"
        "          tolerations:\n"
        "          - key: node-role.kubernetes.io/control-plane\n"
        "            effect: NoSchedule\n"
        "          containers:\n"
        "          - name: etcd-backup\n"
        "            image: registry.k8s.io/etcd:3.5.12-0\n"
        "            command:\n"
        "            - /bin/sh\n"
        "            - -c\n"
        "            - |\n"
        "              etcdctl snapshot save /backup/etcd-$(date +%Y%m%d-%H%M%S).db \\\n"
        "                --endpoints=https://127.0.0.1:2379 \\\n"
        "                --cacert=/etc/kubernetes/pki/etcd/ca.crt \\\n"
        "                --cert=/etc/kubernetes/pki/etcd/server.crt \\\n"
        "                --key=/etc/kubernetes/pki/etcd/server.key\n"
        "              # Upload to S3\n"
        "              aws s3 cp /backup/etcd-*.db s3://k8s-backups/etcd/\n"
        "              # Cleanup local\n"
        "              find /backup -name 'etcd-*.db' -mtime +2 -delete\n"
        "          restartPolicy: OnFailure"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> etcd snapshots contain sensitive data including Secrets "
        "(base64-encoded but not encrypted unless encryption-at-rest is configured). "
        "Encrypt backup files and restrict access to the S3 bucket with IAM policies.",
        styles["warning"],
    ))

    e.append(Paragraph("7.2 Persistent Volume Backup", styles["h2"]))
    e.append(Paragraph(
        "Use VolumeSnapshots for CSI-backed persistent volumes. This provides "
        "point-in-time, crash-consistent copies of application data.",
        styles["body"],
    ))
    e.append(code_block(
        "apiVersion: snapshot.storage.k8s.io/v1\n"
        "kind: VolumeSnapshot\n"
        "metadata:\n"
        "  name: postgres-snap-20260617\n"
        "  namespace: production\n"
        "spec:\n"
        "  volumeSnapshotClassName: csi-aws-vsc\n"
        "  source:\n"
        "    persistentVolumeClaimName: postgres-data\n"
        "---\n"
        "apiVersion: snapshot.storage.k8s.io/v1\n"
        "kind: VolumeSnapshotClass\n"
        "metadata:\n"
        "  name: csi-aws-vsc\n"
        "driver: ebs.csi.aws.com\n"
        "deletionPolicy: Retain\n"
        "parameters:\n"
        "  tagSpecification_1: \"backup=automated\""
    ))

    e.append(Paragraph("Automated backup schedule using Velero:", styles["body"]))
    e.append(code_block(
        "# Install Velero\n"
        "velero install \\\n"
        "  --provider aws \\\n"
        "  --bucket k8s-velero-backups \\\n"
        "  --secret-file ./credentials-velero \\\n"
        "  --backup-location-config region=us-east-1 \\\n"
        "  --snapshot-location-config region=us-east-1 \\\n"
        "  --plugins velero/velero-plugin-for-aws:v1.9.0\n"
        "\n"
        "# Create a scheduled backup (daily at 2 AM)\n"
        "velero schedule create daily-backup \\\n"
        "  --schedule=\"0 2 * * *\" \\\n"
        "  --include-namespaces production,staging \\\n"
        "  --ttl 720h \\\n"
        "  --storage-location default\n"
        "\n"
        "# Verify backups\n"
        "velero backup get\n"
        "velero backup describe daily-backup-20260617020000"
    ))

    e.append(Paragraph("7.3 Disaster Recovery", styles["h2"]))
    e.append(Paragraph(
        "Complete cluster recovery from etcd snapshot. Use this procedure when "
        "the control plane is unrecoverable.",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Stop all control plane components:", styles["numbered"]))
    e.append(code_block(
        "sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/\n"
        "sudo mv /etc/kubernetes/manifests/kube-controller-manager.yaml /tmp/\n"
        "sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/\n"
        "sudo mv /etc/kubernetes/manifests/etcd.yaml /tmp/"
    ))
    e.append(Paragraph("<b>Step 2:</b> Restore etcd from snapshot:", styles["numbered"]))
    e.append(code_block(
        "# Remove old etcd data\n"
        "sudo rm -rf /var/lib/etcd/member\n"
        "\n"
        "# Restore from snapshot\n"
        "sudo etcdctl snapshot restore /backup/etcd-snapshot-latest.db \\\n"
        "  --data-dir=/var/lib/etcd \\\n"
        "  --name=cp-1 \\\n"
        "  --initial-cluster=cp-1=https://10.0.1.10:2380 \\\n"
        "  --initial-advertise-peer-urls=https://10.0.1.10:2380"
    ))
    e.append(Paragraph("<b>Step 3:</b> Restart control plane:", styles["numbered"]))
    e.append(code_block(
        "sudo mv /tmp/etcd.yaml /etc/kubernetes/manifests/\n"
        "sleep 30  # Wait for etcd to start\n"
        "sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/\n"
        "sleep 15\n"
        "sudo mv /tmp/kube-controller-manager.yaml /etc/kubernetes/manifests/\n"
        "sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/\n"
        "\n"
        "# Verify cluster state\n"
        "kubectl get nodes\n"
        "kubectl get pods --all-namespaces"
    ))

    e.append(Paragraph("7.4 Verification Procedures", styles["h2"]))
    e.append(Paragraph(
        "Run these verification steps after every backup and recovery operation:",
        styles["body"],
    ))
    e.append(make_table([
        ["Check", "Command", "Expected Result"],
        ["etcd health", "etcdctl endpoint health", "is healthy: true"],
        ["etcd members", "etcdctl member list", "All members listed"],
        ["API server", "kubectl cluster-info", "Running and accessible"],
        ["Workloads", "kubectl get deploy --all-namespaces", "All desired replicas ready"],
        ["PVCs", "kubectl get pvc --all-namespaces", "All Bound status"],
        ["Services", "kubectl get svc --all-namespaces", "External IPs assigned"],
    ], col_widths=[3*cm, 5*cm, 5.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    for item in [
        "Run backup verification weekly by restoring to a test cluster",
        "Monitor backup job success/failure with Prometheus alerts",
        "Test RTO/RPO quarterly: full cluster restore under 30 minutes",
        "Keep at least 7 days of etcd snapshots available for point-in-time recovery",
        "Document recovery runbooks and keep them updated with each cluster change",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>NOTE:</b> Recovery time depends on cluster size. A 100-node cluster with "
        "5000 resources typically restores in 15-20 minutes. Plan maintenance windows "
        "accordingly. Cross-reference with Section 3.1 for cluster sizing.",
        styles["note"],
    ))
    e.append(PageBreak())
    return e


def section_security(styles):
    e = []
    e.append(Paragraph("8. Security Hardening", styles["h1"]))
    e.append(Paragraph(
        "Security hardening reduces the attack surface of the cluster. Apply these "
        "configurations in order - RBAC first, then network policies, pod security, "
        "and finally secret management.",
        styles["body"],
    ))

    e.append(Paragraph("8.1 RBAC Configuration", styles["h2"]))
    e.append(Paragraph(
        "Role-Based Access Control restricts API access to authorized users and "
        "service accounts. Follow the principle of least privilege.",
        styles["body"],
    ))
    e.append(Paragraph("Namespace-scoped Role for developers:", styles["h3"]))
    e.append(code_block(
        "apiVersion: rbac.authorization.k8s.io/v1\n"
        "kind: Role\n"
        "metadata:\n"
        "  name: developer\n"
        "  namespace: team-alpha\n"
        "rules:\n"
        "- apiGroups: [\"\"]\n"
        "  resources: [\"pods\", \"pods/log\", \"pods/exec\", \"services\", \"configmaps\"]\n"
        "  verbs: [\"get\", \"list\", \"watch\", \"create\", \"update\", \"delete\"]\n"
        "- apiGroups: [\"apps\"]\n"
        "  resources: [\"deployments\", \"replicasets\"]\n"
        "  verbs: [\"get\", \"list\", \"watch\", \"create\", \"update\"]\n"
        "- apiGroups: [\"\"]\n"
        "  resources: [\"secrets\"]\n"
        "  verbs: [\"get\", \"list\"]  # No create/update for secrets\n"
        "---\n"
        "apiVersion: rbac.authorization.k8s.io/v1\n"
        "kind: RoleBinding\n"
        "metadata:\n"
        "  name: developer-binding\n"
        "  namespace: team-alpha\n"
        "subjects:\n"
        "- kind: Group\n"
        "  name: team-alpha-developers\n"
        "  apiGroup: rbac.authorization.k8s.io\n"
        "roleRef:\n"
        "  kind: Role\n"
        "  name: developer\n"
        "  apiGroup: rbac.authorization.k8s.io"
    ))

    e.append(Paragraph("Cluster-wide read-only role for SRE on-call:", styles["h3"]))
    e.append(code_block(
        "apiVersion: rbac.authorization.k8s.io/v1\n"
        "kind: ClusterRole\n"
        "metadata:\n"
        "  name: sre-readonly\n"
        "rules:\n"
        "- apiGroups: [\"*\"]\n"
        "  resources: [\"*\"]\n"
        "  verbs: [\"get\", \"list\", \"watch\"]\n"
        "- apiGroups: [\"\"]\n"
        "  resources: [\"secrets\"]\n"
        "  verbs: []  # Explicitly deny secret access in read-only role\n"
        "---\n"
        "apiVersion: rbac.authorization.k8s.io/v1\n"
        "kind: ClusterRoleBinding\n"
        "metadata:\n"
        "  name: sre-readonly-binding\n"
        "subjects:\n"
        "- kind: Group\n"
        "  name: sre-oncall\n"
        "  apiGroup: rbac.authorization.k8s.io\n"
        "roleRef:\n"
        "  kind: ClusterRole\n"
        "  name: sre-readonly\n"
        "  apiGroup: rbac.authorization.k8s.io"
    ))

    e.append(Paragraph("RBAC audit checklist:", styles["body"]))
    for item in [
        "No ClusterRoleBindings to cluster-admin for regular users",
        "Service accounts have minimal permissions (not default SA)",
        "automountServiceAccountToken: false on pods that do not need API access",
        "Regularly audit RBAC with: kubectl auth can-i --list --as=user@example.com",
        "Use kubectl-who-can plugin to identify overly permissive roles",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph("8.2 Network Policies", styles["h2"]))
    e.append(Paragraph(
        "Network Policies implement microsegmentation - pods can only communicate "
        "with explicitly allowed peers. Start with deny-all, then allow specific traffic.",
        styles["body"],
    ))
    e.append(Paragraph("Default deny-all policy (apply to every namespace):", styles["h3"]))
    e.append(code_block(
        "apiVersion: networking.k8s.io/v1\n"
        "kind: NetworkPolicy\n"
        "metadata:\n"
        "  name: default-deny-all\n"
        "  namespace: production\n"
        "spec:\n"
        "  podSelector: {}  # Applies to all pods\n"
        "  policyTypes:\n"
        "  - Ingress\n"
        "  - Egress"
    ))
    e.append(Paragraph("Allow specific traffic patterns:", styles["h3"]))
    e.append(code_block(
        "apiVersion: networking.k8s.io/v1\n"
        "kind: NetworkPolicy\n"
        "metadata:\n"
        "  name: allow-api-to-db\n"
        "  namespace: production\n"
        "spec:\n"
        "  podSelector:\n"
        "    matchLabels:\n"
        "      app: postgres\n"
        "  policyTypes:\n"
        "  - Ingress\n"
        "  ingress:\n"
        "  - from:\n"
        "    - podSelector:\n"
        "        matchLabels:\n"
        "          app: api-server\n"
        "    ports:\n"
        "    - protocol: TCP\n"
        "      port: 5432\n"
        "---\n"
        "apiVersion: networking.k8s.io/v1\n"
        "kind: NetworkPolicy\n"
        "metadata:\n"
        "  name: allow-dns-egress\n"
        "  namespace: production\n"
        "spec:\n"
        "  podSelector: {}\n"
        "  policyTypes:\n"
        "  - Egress\n"
        "  egress:\n"
        "  - to:\n"
        "    - namespaceSelector:\n"
        "        matchLabels:\n"
        "          kubernetes.io/metadata.name: kube-system\n"
        "      podSelector:\n"
        "        matchLabels:\n"
        "          k8s-app: kube-dns\n"
        "    ports:\n"
        "    - protocol: UDP\n"
        "      port: 53\n"
        "    - protocol: TCP\n"
        "      port: 53"
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> Applying a deny-all policy without allowing DNS egress will "
        "break all service discovery. Always include the DNS egress rule when implementing "
        "default-deny policies. Test in a staging namespace first.",
        styles["warning"],
    ))

    e.append(Paragraph("8.3 Pod Security Standards", styles["h2"]))
    e.append(Paragraph(
        "Pod Security Admission (PSA) enforces security standards at the namespace level. "
        "Apply the restricted profile for production workloads.",
        styles["body"],
    ))
    e.append(code_block(
        "# Label namespace with Pod Security Standards\n"
        "kubectl label namespace production \\\n"
        "  pod-security.kubernetes.io/enforce=restricted \\\n"
        "  pod-security.kubernetes.io/audit=restricted \\\n"
        "  pod-security.kubernetes.io/warn=restricted\n"
        "\n"
        "# For system namespaces that need elevated privileges:\n"
        "kubectl label namespace kube-system \\\n"
        "  pod-security.kubernetes.io/enforce=privileged"
    ))

    e.append(Paragraph("Compliant pod specification (restricted profile):", styles["body"]))
    e.append(code_block(
        "apiVersion: v1\n"
        "kind: Pod\n"
        "metadata:\n"
        "  name: secure-app\n"
        "spec:\n"
        "  securityContext:\n"
        "    runAsNonRoot: true\n"
        "    runAsUser: 1000\n"
        "    runAsGroup: 1000\n"
        "    fsGroup: 1000\n"
        "    seccompProfile:\n"
        "      type: RuntimeDefault\n"
        "  containers:\n"
        "  - name: app\n"
        "    image: registry.example.com/app:v1.0.0\n"
        "    securityContext:\n"
        "      allowPrivilegeEscalation: false\n"
        "      readOnlyRootFilesystem: true\n"
        "      capabilities:\n"
        "        drop:\n"
        "        - ALL\n"
        "    volumeMounts:\n"
        "    - name: tmp\n"
        "      mountPath: /tmp\n"
        "  volumes:\n"
        "  - name: tmp\n"
        "    emptyDir: {}"
    ))

    e.append(make_table([
        ["Security Control", "Restricted", "Baseline", "Privileged"],
        ["HostNetwork", "Forbidden", "Forbidden", "Allowed"],
        ["HostPID/IPC", "Forbidden", "Forbidden", "Allowed"],
        ["Privileged Containers", "Forbidden", "Forbidden", "Allowed"],
        ["Root User", "Forbidden", "Allowed", "Allowed"],
        ["Capabilities", "Drop ALL only", "Add NET_BIND", "Any"],
        ["Volume Types", "Limited set", "Most types", "Any"],
    ], col_widths=[4*cm, 3.5*cm, 3.5*cm, 3.5*cm]))

    e.append(Paragraph("8.4 Secret Management", styles["h2"]))
    e.append(Paragraph(
        "Kubernetes Secrets are base64-encoded but not encrypted by default. "
        "Implement encryption at rest and consider external secret management.",
        styles["body"],
    ))
    e.append(Paragraph("Enable encryption at rest:", styles["h3"]))
    e.append(code_block(
        "# /etc/kubernetes/enc/encryption-config.yaml\n"
        "apiVersion: apiserver.config.k8s.io/v1\n"
        "kind: EncryptionConfiguration\n"
        "resources:\n"
        "- resources:\n"
        "  - secrets\n"
        "  - configmaps\n"
        "  providers:\n"
        "  - kms:\n"
        "      apiVersion: v2\n"
        "      name: aws-kms\n"
        "      endpoint: unix:///run/kmsplugin/socket.sock\n"
        "      timeout: 3s\n"
        "  - identity: {}  # Fallback for reading unencrypted secrets"
    ))

    e.append(Paragraph("External Secrets Operator for HashiCorp Vault:", styles["h3"]))
    e.append(code_block(
        "# Install External Secrets Operator\n"
        "helm install external-secrets external-secrets/external-secrets \\\n"
        "  --namespace external-secrets \\\n"
        "  --create-namespace\n"
        "\n"
        "# Configure Vault SecretStore\n"
        "apiVersion: external-secrets.io/v1beta1\n"
        "kind: ClusterSecretStore\n"
        "metadata:\n"
        "  name: vault-backend\n"
        "spec:\n"
        "  provider:\n"
        "    vault:\n"
        "      server: https://vault.example.com\n"
        "      path: secret\n"
        "      version: v2\n"
        "      auth:\n"
        "        kubernetes:\n"
        "          mountPath: kubernetes\n"
        "          role: external-secrets\n"
        "---\n"
        "# Sync a secret from Vault\n"
        "apiVersion: external-secrets.io/v1beta1\n"
        "kind: ExternalSecret\n"
        "metadata:\n"
        "  name: db-credentials\n"
        "  namespace: production\n"
        "spec:\n"
        "  refreshInterval: 1h\n"
        "  secretStoreRef:\n"
        "    name: vault-backend\n"
        "    kind: ClusterSecretStore\n"
        "  target:\n"
        "    name: db-credentials\n"
        "    creationPolicy: Owner\n"
        "  data:\n"
        "  - secretKey: username\n"
        "    remoteRef:\n"
        "      key: production/database\n"
        "      property: username\n"
        "  - secretKey: password\n"
        "    remoteRef:\n"
        "      key: production/database\n"
        "      property: password"
    ))

    e.append(Paragraph("Security hardening checklist:", styles["body"]))
    for item in [
        "Encryption at rest enabled for Secrets and ConfigMaps",
        "RBAC configured with least privilege for all users and service accounts",
        "Network Policies deny-all default with explicit allow rules",
        "Pod Security Standards enforced at restricted level in production",
        "Container images scanned for vulnerabilities before deployment",
        "Image pull policies set to Always for production workloads",
        "Audit logging enabled on API server with 30-day retention",
        "etcd access restricted to control plane nodes only",
        "Service mesh (Istio/Linkerd) for mTLS between services",
        "Regular penetration testing and CIS benchmark audits",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>NOTE:</b> After enabling encryption at rest, existing secrets remain "
        "unencrypted. Run <font face='Courier'>kubectl get secrets --all-namespaces "
        "-o json | kubectl replace -f -</font> to re-encrypt all existing secrets. "
        "This is a one-time operation that must complete before removing the identity "
        "provider from the encryption config.",
        styles["note"],
    ))
    e.append(PageBreak())
    return e



def section_appendix_a(styles):
    """Appendix A: Command Reference"""
    e = []
    e.append(Paragraph("Appendix A: kubectl Command Reference", styles["h1"]))
    e.append(Paragraph(
        "Quick reference for commonly used kubectl commands organized by operation type.",
        styles["body"],
    ))

    e.append(Paragraph("A.1 Cluster Management", styles["h2"]))
    e.append(code_block(
        "# Cluster information\n"
        "kubectl cluster-info\n"
        "kubectl cluster-info dump > cluster-dump.txt\n"
        "kubectl get componentstatuses\n"
        "kubectl api-resources\n"
        "kubectl api-versions\n"
        "\n"
        "# Node management\n"
        "kubectl get nodes -o wide\n"
        "kubectl describe node <node-name>\n"
        "kubectl cordon <node-name>          # Mark unschedulable\n"
        "kubectl uncordon <node-name>        # Mark schedulable\n"
        "kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data\n"
        "kubectl taint nodes <node> key=value:NoSchedule\n"
        "kubectl taint nodes <node> key=value:NoSchedule-  # Remove taint\n"
        "\n"
        "# Resource usage\n"
        "kubectl top nodes\n"
        "kubectl top pods --all-namespaces --sort-by=memory\n"
        "kubectl top pods -n <namespace> --containers"
    ))

    e.append(Paragraph("A.2 Workload Management", styles["h2"]))
    e.append(code_block(
        "# Deployments\n"
        "kubectl get deployments -n <namespace>\n"
        "kubectl describe deployment <name> -n <namespace>\n"
        "kubectl scale deployment <name> --replicas=5 -n <namespace>\n"
        "kubectl set image deployment/<name> container=image:tag -n <namespace>\n"
        "kubectl rollout status deployment/<name> -n <namespace>\n"
        "kubectl rollout history deployment/<name> -n <namespace>\n"
        "kubectl rollout undo deployment/<name> -n <namespace>\n"
        "kubectl rollout undo deployment/<name> --to-revision=3 -n <namespace>\n"
        "kubectl rollout restart deployment/<name> -n <namespace>\n"
        "\n"
        "# Pods\n"
        "kubectl get pods -n <namespace> -o wide\n"
        "kubectl get pods --field-selector=status.phase=Failed -A\n"
        "kubectl describe pod <pod-name> -n <namespace>\n"
        "kubectl logs <pod-name> -n <namespace> -f --tail=100\n"
        "kubectl logs <pod-name> -n <namespace> -c <container> --previous\n"
        "kubectl exec -it <pod-name> -n <namespace> -- /bin/sh\n"
        "kubectl port-forward <pod-name> 8080:80 -n <namespace>\n"
        "kubectl cp <pod-name>:/path/file ./local-file -n <namespace>\n"
        "\n"
        "# Jobs and CronJobs\n"
        "kubectl get jobs -n <namespace>\n"
        "kubectl get cronjobs -n <namespace>\n"
        "kubectl create job manual-job --from=cronjob/<name> -n <namespace>"
    ))

    e.append(Paragraph("A.3 Networking Commands", styles["h2"]))
    e.append(code_block(
        "# Services\n"
        "kubectl get svc -n <namespace>\n"
        "kubectl get endpoints -n <namespace>\n"
        "kubectl describe svc <name> -n <namespace>\n"
        "\n"
        "# Ingress\n"
        "kubectl get ingress -n <namespace>\n"
        "kubectl describe ingress <name> -n <namespace>\n"
        "\n"
        "# Network Policies\n"
        "kubectl get networkpolicies -n <namespace>\n"
        "kubectl describe networkpolicy <name> -n <namespace>\n"
        "\n"
        "# DNS debugging\n"
        "kubectl run dnsutils --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -it --rm -- nslookup kubernetes.default\n"
        "kubectl exec -it <pod> -- cat /etc/resolv.conf\n"
        "\n"
        "# Connectivity testing\n"
        "kubectl run netshoot --image=nicolaka/netshoot -it --rm -- bash\n"
        "# Inside: curl, dig, nslookup, tcpdump, iperf3 available"
    ))

    e.append(Paragraph("A.4 Storage Commands", styles["h2"]))
    e.append(code_block(
        "# Persistent Volumes and Claims\n"
        "kubectl get pv\n"
        "kubectl get pvc -n <namespace>\n"
        "kubectl describe pvc <name> -n <namespace>\n"
        "\n"
        "# Storage Classes\n"
        "kubectl get storageclass\n"
        "kubectl describe storageclass <name>\n"
        "kubectl patch storageclass <name> -p '{\"metadata\": {\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'\n"
        "\n"
        "# Volume Snapshots\n"
        "kubectl get volumesnapshots -n <namespace>\n"
        "kubectl get volumesnapshotcontents\n"
        "kubectl describe volumesnapshot <name> -n <namespace>"
    ))

    e.append(Paragraph("A.5 RBAC and Security Commands", styles["h2"]))
    e.append(code_block(
        "# Check permissions\n"
        "kubectl auth can-i create pods -n <namespace>\n"
        "kubectl auth can-i --list --as=user@example.com\n"
        "kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa-name>\n"
        "\n"
        "# Service Accounts\n"
        "kubectl get serviceaccounts -n <namespace>\n"
        "kubectl create token <sa-name> -n <namespace>\n"
        "\n"
        "# Secrets\n"
        "kubectl get secrets -n <namespace>\n"
        "kubectl create secret generic <name> --from-literal=key=value -n <namespace>\n"
        "kubectl create secret tls <name> --cert=cert.pem --key=key.pem -n <namespace>\n"
        "kubectl get secret <name> -n <namespace> -o jsonpath='{.data.key}' | base64 -d\n"
        "\n"
        "# Pod Security\n"
        "kubectl label namespace <ns> pod-security.kubernetes.io/enforce=restricted\n"
        "kubectl get ns --show-labels | grep pod-security"
    ))

    e.append(make_table([
        ["Operation", "Shorthand", "Example"],
        ["Get all resources", "kubectl get all", "kubectl get all -n prod"],
        ["Watch changes", "-w flag", "kubectl get pods -w"],
        ["Output formats", "-o yaml/json/wide", "kubectl get pod x -o yaml"],
        ["Label selector", "-l key=value", "kubectl get pods -l app=nginx"],
        ["All namespaces", "-A", "kubectl get pods -A"],
        ["Dry run", "--dry-run=client -o yaml", "Generate YAML without applying"],
    ], col_widths=[3.5*cm, 4*cm, 6*cm]))
    e.append(PageBreak())
    return e


def section_appendix_b(styles):
    """Appendix B: Troubleshooting Flowcharts and Runbooks"""
    e = []
    e.append(Paragraph("Appendix B: Operational Runbooks", styles["h1"]))
    e.append(Paragraph(
        "Step-by-step runbooks for common operational scenarios. Each runbook includes "
        "decision criteria, commands, and escalation paths.",
        styles["body"],
    ))

    e.append(Paragraph("B.1 Runbook: Node Not Ready", styles["h2"]))
    e.append(Paragraph(
        "Use this runbook when a node transitions to NotReady state and does not "
        "recover within 5 minutes.",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Identify the affected node and duration:", styles["numbered"]))
    e.append(code_block(
        "kubectl get nodes\n"
        "kubectl describe node <node-name> | grep -A 10 Conditions\n"
        "\n"
        "# Check when node went NotReady\n"
        "kubectl get events --field-selector involvedObject.name=<node-name> \\\n"
        "  --sort-by='.lastTimestamp'"
    ))
    e.append(Paragraph("<b>Step 2:</b> Check kubelet status on the node:", styles["numbered"]))
    e.append(code_block(
        "# SSH to the node\n"
        "ssh admin@<node-ip>\n"
        "\n"
        "# Check kubelet status\n"
        "sudo systemctl status kubelet\n"
        "sudo journalctl -u kubelet --since '10 minutes ago' | tail -50\n"
        "\n"
        "# Check system resources\n"
        "free -h\n"
        "df -h\n"
        "top -bn1 | head -20"
    ))
    e.append(Paragraph("<b>Step 3:</b> Common causes and fixes:", styles["numbered"]))
    e.append(make_table([
        ["Symptom in kubelet logs", "Cause", "Fix"],
        ["certificate has expired", "Kubelet cert expired", "kubeadm certs renew all"],
        ["failed to connect to apiserver", "Network partition", "Check firewall, NIC status"],
        ["disk pressure", "Disk full", "Clean images: crictl rmi --prune"],
        ["memory pressure", "OOM conditions", "Identify memory-heavy pods, increase node"],
        ["PLEG not healthy", "Container runtime stuck", "Restart containerd"],
    ], col_widths=[4.5*cm, 3.5*cm, 5.5*cm]))
    e.append(Spacer(1, 0.3*cm))
    e.append(Paragraph("<b>Step 4:</b> If kubelet cannot be recovered:", styles["numbered"]))
    e.append(code_block(
        "# Cordon and drain the node\n"
        "kubectl cordon <node-name>\n"
        "kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --timeout=120s\n"
        "\n"
        "# If drain times out (PDB blocking), force eviction:\n"
        "kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force\n"
        "\n"
        "# Remove the node from cluster\n"
        "kubectl delete node <node-name>\n"
        "\n"
        "# On the node, reset kubeadm state\n"
        "sudo kubeadm reset -f\n"
        "sudo rm -rf /etc/cni/net.d\n"
        "\n"
        "# Rejoin the cluster\n"
        "sudo kubeadm join <api-endpoint> --token <token> --discovery-token-ca-cert-hash <hash>"
    ))
    e.append(Paragraph(
        "<b>WARNING:</b> Forcing drain bypasses PodDisruptionBudgets. Only use "
        "<font face='Courier'>--force</font> if the node is truly unrecoverable and "
        "pods are already not running. Verify workload health after forced drain.",
        styles["warning"],
    ))

    e.append(Paragraph("B.2 Runbook: High API Server Latency", styles["h2"]))
    e.append(Paragraph(
        "Use when API server response times exceed 1 second for non-LIST operations "
        "or 5 seconds for LIST operations.",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Confirm the issue with metrics:", styles["numbered"]))
    e.append(code_block(
        "# Check API server latency (99th percentile)\n"
        "# PromQL: histogram_quantile(0.99,\n"
        "#   sum(rate(apiserver_request_duration_seconds_bucket{verb!=\"WATCH\"}[5m])) by (le, verb))\n"
        "\n"
        "# Check request rates\n"
        "kubectl get --raw /metrics | grep apiserver_request_total | head -20\n"
        "\n"
        "# Check for many pending requests\n"
        "kubectl get --raw /metrics | grep apiserver_current_inflight_requests"
    ))
    e.append(Paragraph("<b>Step 2:</b> Check etcd performance:", styles["numbered"]))
    e.append(code_block(
        "# etcd latency metrics\n"
        "# PromQL: histogram_quantile(0.99,\n"
        "#   rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))\n"
        "\n"
        "# Should be < 10ms. If > 50ms, etcd disk is the bottleneck.\n"
        "\n"
        "# Check etcd database size\n"
        "etcdctl endpoint status --write-table\n"
        "\n"
        "# If DB size > 4GB, compact and defragment:\n"
        "etcdctl compact $(etcdctl endpoint status -w json | jq '.[0].Status.header.revision')\n"
        "etcdctl defrag --endpoints=https://127.0.0.1:2379"
    ))
    e.append(Paragraph("<b>Step 3:</b> Check for expensive LIST operations:", styles["numbered"]))
    e.append(code_block(
        "# Enable audit logging to find expensive requests\n"
        "# Look for requests with large response sizes:\n"
        "grep 'responseStatus' /var/log/kubernetes/audit.log | \\\n"
        "  jq -r 'select(.responseStatus.code==200) | [.verb, .requestURI, .responseObject.metadata.resourceVersion] | @csv' | \\\n"
        "  sort -t, -k3 -rn | head -20\n"
        "\n"
        "# Common culprits:\n"
        "# - Controllers listing all pods without field selectors\n"
        "# - Monitoring tools scraping full resource lists\n"
        "# - Custom controllers without informer caches"
    ))
    e.append(Paragraph(
        "<b>NOTE:</b> If API server latency correlates with specific times of day, "
        "check for CronJobs or batch processes that create many resources simultaneously. "
        "Consider implementing API Priority and Fairness (APF) to prevent queue starvation. "
        "Cross-reference with Section 5.3 alert rules for detection.",
        styles["note"],
    ))

    e.append(Paragraph("B.3 Runbook: Certificate Expiry", styles["h2"]))
    e.append(Paragraph(
        "Kubernetes certificates expire after 1 year by default. Plan rotation "
        "before expiry to avoid cluster outage.",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Check certificate expiration dates:", styles["numbered"]))
    e.append(code_block(
        "# Check all kubeadm-managed certificates\n"
        "sudo kubeadm certs check-expiration\n"
        "\n"
        "# Example output:\n"
        "# CERTIFICATE                EXPIRES                  RESIDUAL TIME\n"
        "# admin.conf                 Jun 15, 2027 00:00 UTC   364d\n"
        "# apiserver                  Jun 15, 2027 00:00 UTC   364d\n"
        "# apiserver-etcd-client      Jun 15, 2027 00:00 UTC   364d\n"
        "# apiserver-kubelet-client   Jun 15, 2027 00:00 UTC   364d\n"
        "# controller-manager.conf    Jun 15, 2027 00:00 UTC   364d\n"
        "# etcd-healthcheck-client    Jun 15, 2027 00:00 UTC   364d\n"
        "# etcd-peer                  Jun 15, 2027 00:00 UTC   364d\n"
        "# etcd-server                Jun 15, 2027 00:00 UTC   364d\n"
        "# front-proxy-client         Jun 15, 2027 00:00 UTC   364d\n"
        "# scheduler.conf             Jun 15, 2027 00:00 UTC   364d"
    ))
    e.append(Paragraph("<b>Step 2:</b> Renew certificates:", styles["numbered"]))
    e.append(code_block(
        "# Renew all certificates\n"
        "sudo kubeadm certs renew all\n"
        "\n"
        "# Restart control plane components to pick up new certs\n"
        "sudo crictl pods --name kube-apiserver -q | xargs sudo crictl stopp\n"
        "sudo crictl pods --name kube-controller-manager -q | xargs sudo crictl stopp\n"
        "sudo crictl pods --name kube-scheduler -q | xargs sudo crictl stopp\n"
        "sudo crictl pods --name etcd -q | xargs sudo crictl stopp\n"
        "\n"
        "# Update kubeconfig\n"
        "sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config\n"
        "sudo chown $(id -u):$(id -g) $HOME/.kube/config\n"
        "\n"
        "# Verify\n"
        "kubectl get nodes"
    ))
    e.append(Paragraph(
        "<b>WARNING:</b> Certificate renewal causes brief API server unavailability. "
        "Schedule during maintenance window. For HA clusters, rotate one control plane "
        "node at a time. Notify all teams using kubectl before starting rotation.",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e


def section_appendix_c(styles):
    """Appendix C: Configuration Templates and Environment Variables"""
    e = []
    e.append(Paragraph("Appendix C: Configuration Templates", styles["h1"]))
    e.append(Paragraph(
        "Reference configurations for common deployment patterns. Copy and adapt "
        "these templates for your environment.",
        styles["body"],
    ))

    e.append(Paragraph("C.1 Production-Ready Deployment Template", styles["h2"]))
    e.append(code_block(
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: {{ .Values.app.name }}\n"
        "  namespace: {{ .Values.namespace }}\n"
        "  labels:\n"
        "    app.kubernetes.io/name: {{ .Values.app.name }}\n"
        "    app.kubernetes.io/version: {{ .Values.app.version }}\n"
        "    app.kubernetes.io/managed-by: helm\n"
        "spec:\n"
        "  replicas: {{ .Values.replicas }}\n"
        "  revisionHistoryLimit: 5\n"
        "  strategy:\n"
        "    type: RollingUpdate\n"
        "    rollingUpdate:\n"
        "      maxSurge: 25%\n"
        "      maxUnavailable: 0\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app.kubernetes.io/name: {{ .Values.app.name }}\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app.kubernetes.io/name: {{ .Values.app.name }}\n"
        "        app.kubernetes.io/version: {{ .Values.app.version }}\n"
        "      annotations:\n"
        "        prometheus.io/scrape: \"true\"\n"
        "        prometheus.io/port: \"9090\"\n"
        "        prometheus.io/path: /metrics\n"
        "    spec:\n"
        "      serviceAccountName: {{ .Values.app.name }}\n"
        "      automountServiceAccountToken: false\n"
        "      securityContext:\n"
        "        runAsNonRoot: true\n"
        "        runAsUser: 1000\n"
        "        fsGroup: 1000\n"
        "        seccompProfile:\n"
        "          type: RuntimeDefault\n"
        "      topologySpreadConstraints:\n"
        "      - maxSkew: 1\n"
        "        topologyKey: topology.kubernetes.io/zone\n"
        "        whenUnsatisfiable: DoNotSchedule\n"
        "        labelSelector:\n"
        "          matchLabels:\n"
        "            app.kubernetes.io/name: {{ .Values.app.name }}\n"
        "      containers:\n"
        "      - name: {{ .Values.app.name }}\n"
        "        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}\n"
        "        imagePullPolicy: Always\n"
        "        ports:\n"
        "        - name: http\n"
        "          containerPort: 8080\n"
        "        - name: metrics\n"
        "          containerPort: 9090\n"
        "        env:\n"
        "        - name: POD_NAME\n"
        "          valueFrom:\n"
        "            fieldRef:\n"
        "              fieldPath: metadata.name\n"
        "        - name: POD_NAMESPACE\n"
        "          valueFrom:\n"
        "            fieldRef:\n"
        "              fieldPath: metadata.namespace\n"
        "        envFrom:\n"
        "        - configMapRef:\n"
        "            name: {{ .Values.app.name }}-config\n"
        "        - secretRef:\n"
        "            name: {{ .Values.app.name }}-secrets\n"
        "        resources:\n"
        "          requests:\n"
        "            cpu: {{ .Values.resources.requests.cpu }}\n"
        "            memory: {{ .Values.resources.requests.memory }}\n"
        "          limits:\n"
        "            cpu: {{ .Values.resources.limits.cpu }}\n"
        "            memory: {{ .Values.resources.limits.memory }}\n"
        "        readinessProbe:\n"
        "          httpGet:\n"
        "            path: /ready\n"
        "            port: http\n"
        "          initialDelaySeconds: 10\n"
        "          periodSeconds: 5\n"
        "          failureThreshold: 3\n"
        "        livenessProbe:\n"
        "          httpGet:\n"
        "            path: /health\n"
        "            port: http\n"
        "          initialDelaySeconds: 30\n"
        "          periodSeconds: 15\n"
        "          failureThreshold: 3\n"
        "        startupProbe:\n"
        "          httpGet:\n"
        "            path: /health\n"
        "            port: http\n"
        "          failureThreshold: 30\n"
        "          periodSeconds: 5\n"
        "        lifecycle:\n"
        "          preStop:\n"
        "            exec:\n"
        "              command: [\"sh\", \"-c\", \"sleep 10\"]\n"
        "        securityContext:\n"
        "          allowPrivilegeEscalation: false\n"
        "          readOnlyRootFilesystem: true\n"
        "          capabilities:\n"
        "            drop: [ALL]\n"
        "        volumeMounts:\n"
        "        - name: tmp\n"
        "          mountPath: /tmp\n"
        "      terminationGracePeriodSeconds: 60\n"
        "      volumes:\n"
        "      - name: tmp\n"
        "        emptyDir: {}"
    ))

    e.append(Paragraph("C.2 Environment Variables Reference", styles["h2"]))
    e.append(Paragraph(
        "Standard environment variables injected into all application pods:",
        styles["body"],
    ))
    e.append(make_table([
        ["Variable", "Source", "Description"],
        ["POD_NAME", "fieldRef: metadata.name", "Current pod name"],
        ["POD_NAMESPACE", "fieldRef: metadata.namespace", "Current namespace"],
        ["POD_IP", "fieldRef: status.podIP", "Pod IP address"],
        ["NODE_NAME", "fieldRef: spec.nodeName", "Host node name"],
        ["SERVICE_ACCOUNT", "fieldRef: spec.serviceAccountName", "SA name"],
    ], col_widths=[3.5*cm, 5*cm, 5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Application-specific environment variables:", styles["body"]))
    e.append(make_table([
        ["Variable", "Default", "Description"],
        ["APP_ENV", "production", "Environment name (dev/staging/prod)"],
        ["APP_PORT", "8080", "HTTP listen port"],
        ["APP_LOG_LEVEL", "info", "Logging level (debug/info/warn/error)"],
        ["APP_LOG_FORMAT", "json", "Log output format (json/text)"],
        ["DB_HOST", "postgres.db.svc", "Database host"],
        ["DB_PORT", "5432", "Database port"],
        ["DB_NAME", "appdb", "Database name"],
        ["DB_POOL_SIZE", "20", "Connection pool size"],
        ["REDIS_URL", "redis://redis.cache.svc:6379", "Redis connection URL"],
        ["OTEL_ENDPOINT", "http://otel-collector:4317", "OpenTelemetry collector"],
    ], col_widths=[3.5*cm, 4.5*cm, 6*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph(
        "<b>NOTE:</b> Never hardcode secrets in environment variables within the "
        "deployment manifest. Use Secret references or External Secrets Operator. "
        "See Section 8.4 for proper secret injection patterns.",
        styles["note"],
    ))

    e.append(Paragraph("C.3 Horizontal Pod Autoscaler Template", styles["h2"]))
    e.append(code_block(
        "apiVersion: autoscaling/v2\n"
        "kind: HorizontalPodAutoscaler\n"
        "metadata:\n"
        "  name: api-server-hpa\n"
        "  namespace: production\n"
        "spec:\n"
        "  scaleTargetRef:\n"
        "    apiVersion: apps/v1\n"
        "    kind: Deployment\n"
        "    name: api-server\n"
        "  minReplicas: 3\n"
        "  maxReplicas: 20\n"
        "  behavior:\n"
        "    scaleUp:\n"
        "      stabilizationWindowSeconds: 60\n"
        "      policies:\n"
        "      - type: Percent\n"
        "        value: 100\n"
        "        periodSeconds: 60\n"
        "    scaleDown:\n"
        "      stabilizationWindowSeconds: 300\n"
        "      policies:\n"
        "      - type: Pods\n"
        "        value: 1\n"
        "        periodSeconds: 120\n"
        "  metrics:\n"
        "  - type: Resource\n"
        "    resource:\n"
        "      name: cpu\n"
        "      target:\n"
        "        type: Utilization\n"
        "        averageUtilization: 70\n"
        "  - type: Resource\n"
        "    resource:\n"
        "      name: memory\n"
        "      target:\n"
        "        type: Utilization\n"
        "        averageUtilization: 80\n"
        "  - type: Pods\n"
        "    pods:\n"
        "      metric:\n"
        "        name: http_requests_per_second\n"
        "      target:\n"
        "        type: AverageValue\n"
        "        averageValue: \"1000\""
    ))

    e.append(Paragraph("C.4 PodDisruptionBudget Template", styles["h2"]))
    e.append(code_block(
        "apiVersion: policy/v1\n"
        "kind: PodDisruptionBudget\n"
        "metadata:\n"
        "  name: api-server-pdb\n"
        "  namespace: production\n"
        "spec:\n"
        "  minAvailable: 2  # OR use maxUnavailable: 1\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app.kubernetes.io/name: api-server"
    ))
    e.append(Paragraph(
        "PDB considerations:",
        styles["body"],
    ))
    for item in [
        "Set minAvailable to at least N-1 for N-replica deployments",
        "Use maxUnavailable: 1 for large deployments (simpler to reason about)",
        "PDBs block kubectl drain - set appropriate drain timeout",
        "PDBs do not prevent voluntary pod deletion (kubectl delete pod)",
        "For single-replica deployments, PDB prevents all voluntary disruption",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>WARNING:</b> Misconfigured PDBs can block cluster upgrades and node "
        "maintenance indefinitely. Always test PDB behavior before production deployment. "
        "Monitor <font face='Courier'>kube_poddisruptionbudget_status_pod_disruptions_allowed</font> "
        "metric to detect PDBs blocking disruptions.",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e


def section_appendix_d(styles):
    """Appendix D: Upgrade Procedures"""
    e = []
    e.append(Paragraph("Appendix D: Cluster Upgrade Procedures", styles["h1"]))
    e.append(Paragraph(
        "Kubernetes minor version upgrades (e.g., 1.29 to 1.30) must be performed "
        "one minor version at a time. Skipping versions is not supported.",
        styles["body"],
    ))

    e.append(Paragraph("D.1 Pre-Upgrade Checklist", styles["h2"]))
    for item in [
        "Read the Kubernetes changelog for breaking changes and deprecations",
        "Verify all addon compatibility (CNI, CSI, ingress controller, monitoring)",
        "Take etcd snapshot (see Section 7.1)",
        "Ensure all nodes are in Ready state",
        "Verify no ongoing deployments or migrations",
        "Confirm PodDisruptionBudgets allow at least one disruption per deployment",
        "Test upgrade in staging environment first",
        "Notify all teams of maintenance window",
        "Ensure cluster autoscaler is paused during upgrade",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(code_block(
        "# Pre-upgrade verification script\n"
        "#!/bin/bash\n"
        "set -e\n"
        "\n"
        "echo '=== Pre-Upgrade Checks ==='\n"
        "\n"
        "echo 'Checking node status...'\n"
        "NOT_READY=$(kubectl get nodes | grep -c NotReady || true)\n"
        "if [ \"$NOT_READY\" -gt 0 ]; then\n"
        "  echo \"ERROR: $NOT_READY nodes are NotReady. Fix before upgrading.\"\n"
        "  exit 1\n"
        "fi\n"
        "\n"
        "echo 'Checking for pending pods...'\n"
        "PENDING=$(kubectl get pods -A --field-selector=status.phase=Pending | grep -c '' || true)\n"
        "if [ \"$PENDING\" -gt 1 ]; then\n"
        "  echo \"WARNING: $PENDING pods are Pending\"\n"
        "fi\n"
        "\n"
        "echo 'Checking etcd health...'\n"
        "etcdctl endpoint health\n"
        "\n"
        "echo 'Taking etcd backup...'\n"
        "etcdctl snapshot save /backup/pre-upgrade-$(date +%Y%m%d).db\n"
        "\n"
        "echo 'Current versions:'\n"
        "kubectl version --short\n"
        "kubectl get nodes -o custom-columns=NAME:.metadata.name,VERSION:.status.nodeInfo.kubeletVersion\n"
        "\n"
        "echo '=== All checks passed ==='   "
    ))

    e.append(Paragraph("D.2 Control Plane Upgrade", styles["h2"]))
    e.append(Paragraph("<b>Step 1:</b> Upgrade kubeadm on the first control plane node:", styles["numbered"]))
    e.append(code_block(
        "# Unhold and upgrade kubeadm\n"
        "sudo apt-mark unhold kubeadm\n"
        "sudo apt-get update\n"
        "sudo apt-get install -y kubeadm=1.30.2-1.1\n"
        "sudo apt-mark hold kubeadm\n"
        "\n"
        "# Verify kubeadm version\n"
        "kubeadm version"
    ))
    e.append(Paragraph("<b>Step 2:</b> Plan and apply the upgrade:", styles["numbered"]))
    e.append(code_block(
        "# Dry-run to see what will change\n"
        "sudo kubeadm upgrade plan\n"
        "\n"
        "# Apply the upgrade\n"
        "sudo kubeadm upgrade apply v1.30.2\n"
        "\n"
        "# Expected output:\n"
        "# [upgrade/successful] SUCCESS! Your cluster was upgraded to \"v1.30.2\".\n"
        "# [upgrade/kubelet] Now that your control plane is upgraded, please proceed\n"
        "#   with upgrading your kubelets."
    ))
    e.append(Paragraph("<b>Step 3:</b> Upgrade kubelet and kubectl:", styles["numbered"]))
    e.append(code_block(
        "# Upgrade kubelet and kubectl\n"
        "sudo apt-mark unhold kubelet kubectl\n"
        "sudo apt-get install -y kubelet=1.30.2-1.1 kubectl=1.30.2-1.1\n"
        "sudo apt-mark hold kubelet kubectl\n"
        "\n"
        "# Restart kubelet\n"
        "sudo systemctl daemon-reload\n"
        "sudo systemctl restart kubelet\n"
        "\n"
        "# Verify control plane node version\n"
        "kubectl get nodes"
    ))

    e.append(Paragraph("D.3 Worker Node Upgrade", styles["h2"]))
    e.append(Paragraph(
        "Upgrade worker nodes one at a time (or in small batches if cluster capacity allows). "
        "This ensures workload availability throughout the upgrade.",
        styles["body"],
    ))
    e.append(Paragraph("<b>Step 1:</b> Cordon and drain the worker node:", styles["numbered"]))
    e.append(code_block(
        "kubectl cordon worker-1\n"
        "kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data --timeout=300s\n"
        "\n"
        "# Verify pods have moved\n"
        "kubectl get pods -A -o wide --field-selector spec.nodeName=worker-1"
    ))
    e.append(Paragraph("<b>Step 2:</b> SSH to worker and upgrade packages:", styles["numbered"]))
    e.append(code_block(
        "ssh admin@worker-1\n"
        "\n"
        "# Upgrade kubeadm\n"
        "sudo apt-mark unhold kubeadm\n"
        "sudo apt-get update && sudo apt-get install -y kubeadm=1.30.2-1.1\n"
        "sudo apt-mark hold kubeadm\n"
        "\n"
        "# Upgrade node config\n"
        "sudo kubeadm upgrade node\n"
        "\n"
        "# Upgrade kubelet and kubectl\n"
        "sudo apt-mark unhold kubelet kubectl\n"
        "sudo apt-get install -y kubelet=1.30.2-1.1 kubectl=1.30.2-1.1\n"
        "sudo apt-mark hold kubelet kubectl\n"
        "\n"
        "# Restart kubelet\n"
        "sudo systemctl daemon-reload\n"
        "sudo systemctl restart kubelet"
    ))
    e.append(Paragraph("<b>Step 3:</b> Uncordon the node and verify:", styles["numbered"]))
    e.append(code_block(
        "kubectl uncordon worker-1\n"
        "\n"
        "# Verify node is Ready with new version\n"
        "kubectl get node worker-1\n"
        "\n"
        "# Wait for pods to schedule back\n"
        "sleep 30\n"
        "kubectl get pods -A -o wide --field-selector spec.nodeName=worker-1\n"
        "\n"
        "# Repeat for remaining workers: worker-2, worker-3, ..."
    ))

    e.append(Paragraph("D.4 Post-Upgrade Verification", styles["h2"]))
    e.append(make_table([
        ["Check", "Command", "Expected"],
        ["All nodes upgraded", "kubectl get nodes", "All show v1.30.2"],
        ["System pods healthy", "kubectl get pods -n kube-system", "All Running"],
        ["API server version", "kubectl version", "Server v1.30.2"],
        ["Workloads running", "kubectl get deploy -A", "All READY"],
        ["CNI functional", "kubectl exec test -- ping <pod-ip>", "Success"],
        ["DNS working", "kubectl exec test -- nslookup kubernetes", "Resolves"],
        ["Storage operational", "kubectl get pvc -A", "All Bound"],
        ["Monitoring active", "curl prometheus:9090/-/healthy", "200 OK"],
    ], col_widths=[3.5*cm, 5.5*cm, 4.5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph(
        "<b>NOTE:</b> After upgrading, deprecated APIs may stop working. Run "
        "<font face='Courier'>kubectl deprecations</font> (via pluto or kubent) "
        "before upgrade to identify manifests using deprecated API versions. "
        "Update manifests to use current API versions before the next upgrade.",
        styles["note"],
    ))

    e.append(Paragraph(
        "<b>WARNING:</b> If any post-upgrade check fails, do NOT proceed with "
        "upgrading additional nodes. Diagnose the issue first. If the cluster is "
        "in a broken state, restore from the pre-upgrade etcd snapshot (Section 7.3).",
        styles["warning"],
    ))
    e.append(PageBreak())
    return e



def section_appendix_e(styles):
    """Appendix E: Disaster Scenarios and Recovery Times"""
    e = []
    e.append(Paragraph("Appendix E: Disaster Recovery Scenarios", styles["h1"]))
    e.append(Paragraph(
        "This appendix documents tested disaster recovery scenarios with expected "
        "recovery times and procedures. All scenarios assume proper backups exist "
        "(Section 7).",
        styles["body"],
    ))

    e.append(Paragraph("E.1 Scenario: Complete Control Plane Loss", styles["h2"]))
    e.append(make_table([
        ["Parameter", "Value"],
        ["Severity", "Critical - P1"],
        ["Impact", "No new deployments, no scaling, no API access"],
        ["Worker workloads", "Continue running (kubelet autonomous)"],
        ["RTO Target", "30 minutes"],
        ["RPO Target", "6 hours (last etcd backup)"],
        ["Prerequisites", "etcd snapshot, PKI backup, kubeadm config"],
    ], col_widths=[4*cm, 10*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(Paragraph("Recovery procedure:", styles["body"]))
    e.append(Paragraph("<b>Step 1:</b> Provision new control plane node with same OS and containerd:", styles["numbered"]))
    e.append(code_block(
        "# On new control plane node\n"
        "sudo apt-get install -y containerd.io kubelet=1.30.2-1.1 kubeadm=1.30.2-1.1 kubectl=1.30.2-1.1\n"
        "sudo apt-mark hold kubelet kubeadm kubectl\n"
        "\n"
        "# Restore PKI certificates\n"
        "sudo mkdir -p /etc/kubernetes/pki/etcd\n"
        "sudo cp /backup/pki/* /etc/kubernetes/pki/\n"
        "sudo cp /backup/pki/etcd/* /etc/kubernetes/pki/etcd/"
    ))
    e.append(Paragraph("<b>Step 2:</b> Restore etcd and reinitialize control plane:", styles["numbered"]))
    e.append(code_block(
        "# Restore etcd snapshot\n"
        "sudo etcdctl snapshot restore /backup/etcd-latest.db \\\n"
        "  --data-dir=/var/lib/etcd \\\n"
        "  --name=cp-1 \\\n"
        "  --initial-cluster=cp-1=https://10.0.1.10:2380 \\\n"
        "  --initial-advertise-peer-urls=https://10.0.1.10:2380\n"
        "\n"
        "# Initialize control plane with existing PKI\n"
        "sudo kubeadm init --ignore-preflight-errors=DirAvailable--var-lib-etcd \\\n"
        "  --config=/backup/kubeadm-config.yaml\n"
        "\n"
        "# Verify cluster state\n"
        "kubectl get nodes\n"
        "kubectl get pods -A"
    ))
    e.append(Paragraph("<b>Step 3:</b> Reconnect worker nodes (if needed):", styles["numbered"]))
    e.append(code_block(
        "# Workers may reconnect automatically if certificates are valid\n"
        "# If not, on each worker:\n"
        "sudo systemctl restart kubelet\n"
        "\n"
        "# Verify all nodes rejoin\n"
        "kubectl get nodes -w"
    ))

    e.append(Paragraph("E.2 Scenario: Single Worker Node Failure", styles["h2"]))
    e.append(make_table([
        ["Parameter", "Value"],
        ["Severity", "Medium - P3"],
        ["Impact", "Reduced capacity, pods rescheduled"],
        ["Auto-recovery", "Yes (if replicas > 1)"],
        ["RTO Target", "5 minutes (auto) / 15 minutes (manual)"],
        ["RPO Target", "0 (stateless) / backup age (stateful)"],
    ], col_widths=[4*cm, 10*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(code_block(
        "# Kubernetes automatically reschedules pods from failed nodes after 5 minutes\n"
        "# (pod-eviction-timeout default)\n"
        "\n"
        "# To expedite recovery:\n"
        "kubectl delete node <failed-node>\n"
        "\n"
        "# Verify pods are rescheduled\n"
        "kubectl get pods -A -o wide | grep -v Running\n"
        "\n"
        "# For stateful workloads with PVCs:\n"
        "# 1. Ensure PV is available (not bound to old pod)\n"
        "kubectl get pv | grep <pvc-name>\n"
        "# 2. If stuck in Terminating, force delete old pod:\n"
        "kubectl delete pod <pod> --grace-period=0 --force\n"
        "# 3. New pod will bind to existing PV (if same zone)"
    ))

    e.append(Paragraph("E.3 Scenario: etcd Data Corruption", styles["h2"]))
    e.append(Paragraph(
        "<b>Symptoms:</b> API server returns inconsistent data, etcd logs show "
        "checksum errors, cluster behavior is unpredictable.",
        styles["body"],
    ))
    e.append(code_block(
        "# Detect corruption\n"
        "etcdctl endpoint health --cluster\n"
        "etcdctl check perf --load='s'\n"
        "\n"
        "# If single member is corrupt in multi-member cluster:\n"
        "# 1. Remove corrupt member\n"
        "etcdctl member remove <member-id>\n"
        "\n"
        "# 2. Clear data directory on corrupt node\n"
        "sudo systemctl stop etcd\n"
        "sudo rm -rf /var/lib/etcd/member\n"
        "\n"
        "# 3. Re-add as new member\n"
        "etcdctl member add cp-2 --peer-urls=https://10.0.1.11:2380\n"
        "\n"
        "# 4. Start etcd with --initial-cluster-state=existing\n"
        "sudo systemctl start etcd\n"
        "\n"
        "# If ALL members are corrupt (single-node or full cluster):\n"
        "# Follow full restore procedure from Section 7.3"
    ))

    e.append(Paragraph("E.4 Scenario: Network Partition", styles["h2"]))
    e.append(Paragraph(
        "A network partition isolates a subset of nodes from the control plane. "
        "Pods on isolated nodes continue running but cannot be managed.",
        styles["body"],
    ))
    e.append(make_table([
        ["Partition Type", "Impact", "Auto-Recovery"],
        ["Control plane isolated", "Full API outage", "Yes (when network restores)"],
        ["Workers isolated from CP", "Pods run, no mgmt", "Yes (kubelet reconnects)"],
        ["Workers isolated from each other", "Cross-pod traffic fails", "Partial (CNI heals)"],
        ["etcd members split-brain", "API read-only or down", "Yes (quorum restores)"],
    ], col_widths=[4*cm, 4.5*cm, 5*cm]))
    e.append(Spacer(1, 0.3*cm))

    e.append(code_block(
        "# Diagnose network partition\n"
        "# From control plane:\n"
        "for node in worker-1 worker-2 worker-3; do\n"
        "  echo -n \"$node: \"\n"
        "  timeout 3 nc -zv $node 10250 2>&1 | tail -1\n"
        "done\n"
        "\n"
        "# Check node conditions (NetworkUnavailable)\n"
        "kubectl get nodes -o custom-columns=NAME:.metadata.name,NETWORK:.status.conditions[4].status\n"
        "\n"
        "# Check for split-brain in etcd\n"
        "etcdctl endpoint status --cluster --write-table\n"
        "# All members should have same leader ID\n"
        "\n"
        "# Force node status update after network recovery\n"
        "# (kubelet does this automatically within 40 seconds)"
    ))

    e.append(Paragraph("E.5 Recovery Time Summary", styles["h2"]))
    e.append(make_table([
        ["Scenario", "RTO", "RPO", "Automation Level"],
        ["Single pod crash", "<1 min", "0", "Fully automatic"],
        ["Single node failure", "5 min", "0 (stateless)", "Automatic (rescheduling)"],
        ["Control plane restart", "2-5 min", "0", "Automatic (static pods)"],
        ["etcd single member loss", "10-15 min", "0 (replicated)", "Semi-automatic"],
        ["Full control plane loss", "30 min", "6h (backup)", "Manual procedure"],
        ["Complete cluster loss", "1-2 hours", "6h (backup)", "Manual procedure"],
        ["Multi-AZ outage", "2-4 hours", "24h (cross-region)", "Manual + failover"],
    ], col_widths=[4*cm, 2.5*cm, 3*cm, 4*cm]))
    e.append(Spacer(1, 0.5*cm))

    e.append(Paragraph(
        "<b>NOTE:</b> These RTO/RPO values assume backups are current and tested. "
        "Untested backups should be assumed non-functional. Run quarterly DR drills "
        "to validate recovery procedures and update documentation. See Section 7.4 "
        "for verification procedures.",
        styles["note"],
    ))

    for item in [
        "Document all DR procedures in a runbook accessible outside the cluster",
        "Store recovery credentials in a break-glass account separate from cluster",
        "Maintain infrastructure-as-code for rapid cluster reprovisioning",
        "Test failover to secondary region at least twice per year",
        "Keep offline copy of all manifests (Git repo) for rebuilding without cluster access",
        "Automate DR testing with chaos engineering tools (Litmus, Chaos Mesh)",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Paragraph(
        "<b>WARNING:</b> Never assume a backup is valid without testing restoration. "
        "The most common DR failure mode is discovering during an outage that backups "
        "are incomplete, corrupted, or that restoration procedures are outdated.",
        styles["warning"],
    ))
    return e


def section_revision_history(styles):
    """Document revision history and glossary."""
    e = []
    e.append(Paragraph("Appendix F: Revision History & Glossary", styles["h1"]))

    e.append(Paragraph("F.1 Document Revision History", styles["h2"]))
    e.append(make_table([
        ["Version", "Date", "Author", "Changes"],
        ["2.1", "2026-06-17", "Platform Team", "Added Appendix E (DR scenarios), updated HPA template"],
        ["2.0", "2026-03-01", "Platform Team", "Major rewrite for Kubernetes 1.30, added security section"],
        ["1.9", "2025-11-15", "SRE Team", "Added runbooks appendix, updated monitoring stack"],
        ["1.8", "2025-08-20", "Platform Team", "Migrated from Docker to containerd documentation"],
        ["1.7", "2025-05-10", "SRE Team", "Added backup/recovery section, Velero integration"],
        ["1.6", "2025-02-01", "Platform Team", "Updated RBAC examples, added network policies"],
        ["1.5", "2024-11-01", "Platform Team", "Initial public release for Kubernetes 1.28"],
    ], col_widths=[2*cm, 3*cm, 3.5*cm, 6*cm]))
    e.append(Spacer(1, 0.5*cm))

    e.append(Paragraph("F.2 Glossary of Terms", styles["h2"]))
    terms = [
        ("API Server", "The front-end REST API for the Kubernetes control plane. All cluster operations go through the API server."),
        ("CNI", "Container Network Interface - plugin standard for configuring pod networking. Examples: Calico, Cilium, Flannel."),
        ("CRI", "Container Runtime Interface - plugin standard for container runtimes. Examples: containerd, CRI-O."),
        ("CSI", "Container Storage Interface - plugin standard for storage provisioners. Examples: EBS CSI, NFS CSI."),
        ("DaemonSet", "Ensures a pod runs on every (or selected) node. Used for log collectors, monitoring agents."),
        ("etcd", "Distributed key-value store used as Kubernetes backing store for all cluster data."),
        ("HPA", "Horizontal Pod Autoscaler - automatically scales pod replicas based on metrics."),
        ("Kubelet", "Agent running on each node that ensures containers are running in pods as specified."),
        ("Namespace", "Virtual cluster partition for resource isolation and access control."),
        ("PDB", "PodDisruptionBudget - limits voluntary disruptions to maintain availability during maintenance."),
        ("PV/PVC", "PersistentVolume/PersistentVolumeClaim - abstraction for durable storage in the cluster."),
        ("RBAC", "Role-Based Access Control - authorization mechanism based on roles assigned to users/groups."),
        ("StatefulSet", "Manages stateful applications with stable network identities and persistent storage."),
        ("Taint/Toleration", "Mechanism to repel pods from nodes (taint) unless pods explicitly accept (tolerate)."),
    ]
    for term, definition in terms:
        e.append(Paragraph(f"<b>{term}</b>", styles["body"]))
        e.append(Paragraph(definition, styles["bullet"]))
        e.append(Spacer(1, 2*mm))

    e.append(Spacer(1, 0.5*cm))
    e.append(Paragraph("F.3 Related Documentation", styles["h2"]))
    e.append(Paragraph(
        "The following external resources supplement this manual:",
        styles["body"],
    ))
    for item in [
        "Kubernetes Official Documentation: https://kubernetes.io/docs/",
        "Kubernetes API Reference v1.30: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/",
        "etcd Operations Guide: https://etcd.io/docs/v3.5/op-guide/",
        "Calico Documentation: https://docs.tigera.io/calico/latest/about/",
        "Prometheus Operator: https://prometheus-operator.dev/docs/",
        "Helm Documentation: https://helm.sh/docs/",
        "Velero Backup Documentation: https://velero.io/docs/",
        "CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes",
        "NIST Container Security Guide (SP 800-190)",
        "Internal Wiki: https://wiki.internal.example.com/kubernetes",
    ]:
        e.append(Paragraph(f"\u2022 {item}", styles["bullet"]))

    e.append(Spacer(1, 1*cm))
    e.append(Paragraph(
        "<b>NOTE:</b> This document is maintained in Git at "
        "<font face='Courier'>git@github.com:infra-team/k8s-ops-manual.git</font>. "
        "Submit changes via pull request. All changes require review from at least "
        "one Platform team member and one SRE team member before merge.",
        styles["note"],
    ))
    return e


def main():
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = build_styles()
    elements = []

    elements.extend(build_title_page(styles))
    elements.extend(build_toc(styles))
    elements.extend(section_prerequisites(styles))
    elements.extend(section_installation(styles))
    elements.extend(section_configuration(styles))
    elements.extend(section_deployments(styles))
    elements.extend(section_monitoring(styles))
    elements.extend(section_troubleshooting(styles))
    elements.extend(section_backup(styles))
    elements.extend(section_security(styles))
    elements.extend(section_appendix_a(styles))
    elements.extend(section_appendix_b(styles))
    elements.extend(section_appendix_c(styles))
    elements.extend(section_appendix_d(styles))
    elements.extend(section_appendix_e(styles))
    elements.extend(section_revision_history(styles))

    doc.build(elements)
    print(f"PDF generated at: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
