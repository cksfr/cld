**HADOOP**

**1. Install and Setup Hadoop**



Step 1: Install Java



sudo apt update

sudo apt install openjdk-11-jdk -y

java -version



Should show something like:



openjdk version "11.0.xx"



Step 2: Download Hadoop





wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

tar -xzf hadoop-3.3.6.tar.gz

sudo mv hadoop-3.3.6 /usr/local/hadoop



Step 3: Set Environment Variables



nano ~/.bashrc



export HADOOP\_HOME=/usr/local/hadoop

export PATH=$PATH:$HADOOP\_HOME/bin

export JAVA\_HOME=/usr/lib/jvm/java-11-openjdk-amd64



source ~/.bashrc



**2. Run Hadoop WordCount in Local Mode**



Step 1: Create Input Directory and File



mkdir ~/input

echo "hello hadoop hello world bigdata hadoop" > ~/input/sample.txt



Step 2: Find the Example JAR



ls $HADOOP\_HOME/share/hadoop/mapreduce/



You will see:



hadoop-mapreduce-examples-3.3.6.jar



Step 3: Run WordCount\*\*



Run the Hadoop job \*\*in local mode\*\* (no HDFS required):



hadoop jar $HADOOP\_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount ~/input ~/output



> If the output folder exists:



rm -r ~/output



Step 4: View Output



cat ~/output/part-r-00000



Expected output:



bigdata  1

hadoop   2

hello    2

world    1


**SPARK**



1. **Download Spark**



wget https://downloads.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz



**Step 2 — Extract Spark**



Option 1 — Extract in Downloads:



tar -xzf spark-3.5.3-bin-hadoop3.tgz





Option 2 — Move to `/usr/local` (recommended):





sudo mv spark-3.5.3-bin-hadoop3 /usr/local/spark



**3. Set Environment Variables**



nano ~/.bashrc



export SPARK\_HOME=/usr/local/spark

export PATH=$PATH:$SPARK\_HOME/bin



source ~/.bashrc



**4. Verify Spark Installation**



spark-shell



**5. Prepare Input File for WordCount**



echo "hello spark hello world spark bigdata" > ~/sample.txt



**6. Run WordCount in Spark (Scala Shell)**



1\. Open Spark shell:



spark-shell



2\. Inside the shell, run:



val textFile = sc.textFile("file:///home/$USER/sample.txt")

val counts = textFile.flatMap(line => line.split(" "))

&nbsp;                    .map(word => (word, 1))

&nbsp;                    .reduceByKey(\_ + \_)

counts.collect().foreach(println)



output:



(hello,2)

(spark,2)

(world,1)

(bigdata,1)

