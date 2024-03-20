telnet localhost 8080 <<EOF
PUT /new.html HTTP/1.1

<html>
	<p> Teste </p>
</html>
EOF
