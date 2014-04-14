# monkey patch of String
class String
  def execute
    split("\n").collect(&:strip).reject(&:empty?).join(" && ")
  end
end

PACKAGES = %w(
  rabbitmq-server
)

CONFIGURE = <<-CONFIGURE
/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart
rabbitmqctl add_user async_rabbitmq async_rabbitmq
rabbitmqctl add_vhost async_rabbitmq
rabbitmqctl set_permissions -p async_rabbitmq async_rabbitmq ".*" ".*" ".*"
rabbitmqctl set_user_tags async_rabbitmq administrator
wget --auth-no-challenge --http-user=async_rabbitmq --http-password=async_rabbitmq --output-document=/usr/local/bin/rabbitmqadmin http://127.0.0.1:55672/cli/rabbitmqadmin
chmod +x /usr/local/bin/rabbitmqadmin
rabbitmqadmin --bash-completion > /etc/bash_completion.d/rabbitmqadmin
rabbitmqadmin --vhost=async_rabbitmq -u async_rabbitmq -p async_rabbitmq declare exchange name=tasks type=topic
rabbitmqadmin --vhost=async_rabbitmq -u async_rabbitmq -p async_rabbitmq declare queue name=mail
rabbitmqadmin --vhost=async_rabbitmq -u async_rabbitmq -p async_rabbitmq declare binding source=tasks destination_type=queue destination=mail routing_key=task.mail.*
CONFIGURE

# port mapping (guest => host)
PORTS = {
  # rabbitmq
  5672 => 5672,
  55672 => 55672,
}


Vagrant.configure('2') do |config|

  PORTS.each do |guest_port, host_port|
    config.vm.network "forwarded_port", guest: guest_port, host: host_port
  end

  # Use this box URL
  config.vm.box_url = 'http://files.vagrantup.com/precise64.box'

  # Box to use
  config.vm.box = 'precise64'

  # Allow to use host's SSH settings inside the guest system
  config.ssh.forward_agent = true

  config.vm.provider :virtualbox do |vb|
    vb.customize ['modifyvm', :id, '--memory', '512']
  end

  config.vm.provision :shell,
    keep_color: true,
    inline: 'apt-get update'

  config.vm.provision :shell,
    keep_color: true,
    inline: 'apt-get install -y $*',
    args: PACKAGES

  config.vm.provision :shell,
    keep_color: true,
    inline: CONFIGURE.execute

end
