from pygments.lexer import RegexLexer
from pygments.token import Keyword, Operator


__all__ = ["OSLexer"]


class OSLexer(RegexLexer):
    name = 'OSShell'
    aliases = ['osshell']
    filenames = ['*.osshell']

    tokens = {
        'root': [
            (r'(access|address|aggregate|availability|backup'
             r'|catalog|command|compute|configuration|console|consumer'
             r'|container|credential|domain|ec2|endpoint|extension'
             r'|federation|flavor|floating|group|host|hypervisor'
             r'|identity|image|ip|keypair|mapping|network|object'
             r'|policy|port|project|quota|region|request|role|router'
             r'|security|server|service|snapshot|subnet|token|trust'
             r'|usage|user|volume)', Keyword),
            (r'--(ip-version|project|project-domain|share|no-share'
             r'|name|prefix|zone|property|long|consumer-key'
             r'|consumer-secret|request-secret|verifier|compute|network'
             r'|volume|description|container|snapshot|force|incremental'
             r'|enable|disable|disable-reason|host|service|lines|novnc'
             r'|xvpvnc|spice|rdp|serial|mks|type|or-show|region|ram|id'
             r'|disk|ephemeral|swap|vcpus|rxtx-factor|public|private|subnet'
             r'|port|floating-ip-address|fixed-ip-address|prefix|group-domain'
             r'|user-domain|zone|enable-maintenance|disable-maintenance'
             r'|remote-id|remote-id-file|description|container-format'
             r'|disk-format|min-disk|min-ram|file|volume|force|protected'
             r'|unprotected|public|private|property|tag|project|public-key'
             r'|rules|availability-zone-hint|enable-port-security'
             r'|disable-port-security|external|internal|default|no-default'
             r'|provider-network-type|provider-physical-network'
             r'|provider-segment|transparent-vlan|no-transparent-vlan'
             r'|fixed-ip|no-fixed-ip|binding-profile|no-binding-profile'
             r'|image|volume|flavor|security-group|key-name|property'
             r'|file|user-data|availability-zone|block-device-mapping'
             r'|nic|hint|config-drive|min|max|wait|dhcp|no-dhcp'
             r'|gateway|allocation-pool|dns-nameserver|host-route'
             r'|role|impersonate|expiration|trustor-domain|trustee-domain)',
             Operator)],
    }

