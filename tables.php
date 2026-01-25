<?php
$conn = new mysqli("localhost", "user", "password", "banking");

if ($conn->connect_error) {
    die("Connection failed");
}

$sql = "SELECT * FROM Customers";
$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {
    echo $row['customer_id'] . " ";
    echo $row['name'] . "<br>";
}
?>
