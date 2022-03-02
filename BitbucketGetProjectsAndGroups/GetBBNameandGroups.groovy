#!groovy

/*
* This script prints the Bitbucket projects and
* groups associated with them.
*   __author__ = "Mohd Afnan Qureshi"
*   __maintainer__ = "Mohd Afnan Qureshi"
*   __email__ = "md.afnan1995@gmail.com"
*   __status__ = "Production"
*/

import javax.net.ssl.HttpsURLConnection
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManager
import java.net.URL
import groovy.json.JsonSlurper
import javax.net.ssl.X509TrustManager
import java.security.SecureRandom


/*
* Function to return authentication token
*/
def Auth()
{
    def auth = 'token';
    return auth
}


/*
* Function to bypass SSL certificate check and establish connection
*/
def ConnectAPIUsers(def url)
{
    SSLContext sc = SSLContext.getInstance("SSL")
    def trustAll = [getAcceptedIssuers: {}, checkClientTrusted: { a, b -> }, checkServerTrusted: { a, b -> }]
    sc.init(null, [trustAll as X509TrustManager] as TrustManager[], new SecureRandom())
    HttpsURLConnection.defaultSSLSocketFactory = sc.socketFactory
    HttpsURLConnection con = new URL(url).openConnection() as HttpsURLConnection
    con.setRequestMethod("GET");
    con.setRequestProperty("Authorization", "Bearer ${Auth()}");
    return con;
}


/*
* Function to print groups and projects
*/
String[] getData(){
    def bbURL = 'https://bitbucket.com/rest/api/1.0/projects'
    def groupURL = '/permissions/groups'
    def start = 0
    def limit = 250
    def last_page = false
    def projectKey = [:]

    while(last_page==false)
    {
        def api = ConnectAPIUsers(bbURL + '?limit=' + limit + "&start=" + start);
        def responsecode = api.getResponseCode();

        if(responsecode == 200){
            String data = api.getInputStream().getText();

            if(data.contains("nextPageStart"))
            {
                last_page = false;
                start = start + limit
            }
            else
            {
                last_page = true;
            }

            def list = new JsonSlurper().parseText(data);
            list.values.each
            {
                projectKey[it.key] = it.name
            }
        }
       else{
            println('Error connecting');
            last_page = true;
        }
    }

    last_page = false
    start = 0
    while(last_page==false)
    {
        for(entry in projectKey){
            println("Groups in " + entry.value + ":")
            api = ConnectAPIUsers(bbURL + '/' + entry.key + groupURL + '?limit=' + limit + "&start=" + start);
            responsecode = api.getResponseCode();

            if(responsecode == 200){
                data = api.getInputStream().getText();
                // println(data)
                if(data.contains("nextPageStart"))
                {
                    last_page = false;
                    start = start + limit
                }
                else
                {
                    last_page = true;
                }

                list = new JsonSlurper().parseText(data);
                list.values.each
                {
                    println(it.group.name)
                }
            }
            else{
                println('Error connecting');
                last_page = true;
            }  
        }
    }
}

getData();