<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add Book</title>
</head>
<body>
    <form action="{{ url_for('add') }}" method="POST">
        <label>Book Name</label>
        <input name="title" type="text">
        <label>Book Author</label>
        <input name="author" type="text">
        <label>Rating</label>
        <input name="rating" type="text">
        <button type="submit">Add Book</button>
    </form>
</body>
</html>
