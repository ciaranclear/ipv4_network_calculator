from ipv4_networks.ipv4_networks import make_networks




if __name__ == "__main__":

    networks = [
        ["sales",50],
        ["accounting",100],
        ["managment",25],
        ["administration",12]
    ]

    networks = make_networks(networks, "192.168.0.0", "255.255.255.0", True)
    for network in networks:
        print(network)
        print(networks[network])

    for name, network in networks.items():
        print(f"{'#'*40}")
        print(name)
        print(network)
