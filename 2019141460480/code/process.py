import connection
import config


def tcp_server(ID):
    init_config = config.Config()
    peer = init_config.get_attr(ID)
    peer_s = connection.Connection()
    peer_s.set_num(ID)
    peer_s.set_ip(peer['ip_addr'])
    peer_s.set_server_port(peer['server_port'])
    peer_s.set_client_port(peer['client_port'])
    peer_s.set_share_dir(peer['share_dir'])
    peer_s.set_peer_list(peer['peer_list'])
    peer_s.update_peer_attr()
    peer_s.tcp_server()


def tcp_client(role_num, filename):
    init_config = config.Config()
    peer_ccon = init_config.get_attr(role_num)
    peer_c = connection.Connection()
    peer_c.set_ip(peer_ccon['ip_addr'])
    peer_c.set_server_port(peer_ccon['server_port'])
    peer_c.set_client_port(peer_ccon['client_port'])
    peer_c.set_share_dir(peer_ccon['share_dir'])
    peer_c.set_peer_list(peer_ccon['peer_list'])
    peer_attr = peer_c.update_peer_attr()

    for i in peer_attr:
        print("client query %s" % i['server_port'])
        peer_c.tcp_client_notice(i['ip_addr'], i['server_port'], "get %s %s %s %s" % (
            filename, peer_ccon['server_port'], peer_ccon['ip_addr'], init_config.get_ttl()))
