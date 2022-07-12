# Create Docker image
docker build -t my-mysql .

# Start MySQL container from the image
docker run -d -p 3306:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=supersecret my-mysql
