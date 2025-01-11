# Install virtuoso:
brew install virtuoso
brew unlink  unixodbc   # remove unixodbc isql
brew link    virtuoso   # add    virtuoso isql

# Launch virtuoso:

virtuoso-t -f -c /opt/homebrew/Cellar/virtuoso/7.2.14/var/lib/virtuoso/db/virtuoso.ini

# => Web site at http://localhost:8890
# => SPARQL endpoint at http://localhost:8890/sparql
# => isql and rdf4j connect at localhost:1111 AFAIK

# verify connection with isql

isql

docker pull sibswiss/rdf4j:latest

# FIXME: verify that the option below are authorised/respected by docker
docker run -d \
    -p 8080:8080 \
    -e JAVA_OPTS="-Xms2g -Xmx24g" \
    -v ~/scratch/rdf4j:/var/rdf4j \
    -v ~/scratch/logs:/usr/local/tomcat/logs \
    -v ~/gitlab/sinergiawolfender/common/data/rdf:/var/tmp \
    --cpus=6 \
    sibswiss/rdf4j:latest

# => Web site at http://localhost:8080/rdf4j-workbench/repositories


docker ps # gives container-id
docker stop <container-id>

docker exec -it cf88f09f8758  bash



sed -n -e '1,14000005p' metanetx.ttl  > metanetx_1.ttl 
head -75 metanetx.ttl  > metanetx_2.ttl
sed -n -e '14000006,$p' metanetx.ttl  >> metanetx_2.ttl

docker pull sibswiss/kgsteward-rdf4j:4.3.5

export RDF4J_VERSION=4.3.5
docker run -d -p 8080:8080 -p 1111:1111 -e JAVA_OPTS="-Xms1g -Xmx4g" -v data:/var/rdf4j -v logs:/usr/local/tomcat/logs sibswiss/kgsteward-rdf4j:$RDF4J_VERSION

/opt/homebrew/bin/virtuoso-t -f -c /opt/homebrew/Cellar/virtuoso/7.2.10/var/lib/virtuoso/db/virtuoso.ini

Using Eclipse RDF4J via docker:

# from https://stackoverflow.com/questions/71370039/what-is-is-the-simplest-way-to-setup-a-local-rdf-triple-store-with-sparql-endpoi
docker pull eclipse/rdf4j-workbench:latest
docker run -p 8080:8080 eclipse/rdf4j-workbench:latest
and then access at http://localhost:8080/rdf4j-workbench
podman exec -it 6d2b8f60bb22 /bin/bash



# Fuseki

## Howmebrew default installation seems to hardcode the following two paths:
# FUSEKI_HOME=/opt/homebrew/Cellar/fuseki/5.0.0/libexec
# FUSEKI_BASE=/opt/homebrew/var/fuseki
# which cannot be easily overwritten

# launch fuseki on port 3030
/opt/homebrew/bin/fuseki-server \
    --tdb2 \
    --loc=/Users/mpagni/scratch/fuseki-server \
    --update \
    /ReconXKG


docker run -d \
    -p 8080:8080 \
    -e JAVA_OPTS="-Xms2g -Xmx24g" \
    -v ~/scratch/rdf4j/data:/var/rdf4j \
    -v ~/scratch/rdf4j/logs:/usr/local/tomcat/logs \
    --cpus=4 \
    eclipse/rdf4j-workbench:latest

# curl -X DELETE http://localhost:8080/rdf4j-server/repositories/JLW_Native_Lucene_RDFS
# curl -H 'content-type: text/turtle' --upload-file common/data/config/JLW_Native_Lucene_RDFS.config.ttl http://localhost:8080/rdf4j-server/repositories/JLW_Native_Lucene_RDFS
uv run ./kgsteward /Users/mpagni/gitlab.sib.swiss/sinergiawolfender/common/data/config/JLW_Native_Lucene_RDFS.yaml


-Xss:512k


A link to similar preocupation: https://epimorphics.medium.com/regression-testing-and-data-checking-using-sparql-c5d5b4c11724

uv build
uv publish --token pypi-AgEIcHlwaS5vcmcCJGI0MDY5MzljLTM0MTgtNDljMi05OTI3LWI3OWJkZDVjMDc5YwACKlszLCJhY2VjNWJjNi1iN2Q5LTRiYjUtYmQ3OS1iMTQ1MGY5ZTNhMGYiXQAABiCS6XsXlcMNvBy3pkSpdpXafKVeaelCrZN6TuksOqrBqw

git tag -a "2.0.0" -m "kgsteward 2.0.0"
git push origin "2.0.0"
 
