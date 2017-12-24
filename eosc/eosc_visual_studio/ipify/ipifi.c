#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

void herror(CURL*, const char*, const char*);

int main(int argc, char *argv[]) {

  CURL *curl;
  CURLcode res;
  curl_global_init(CURL_GLOBAL_DEFAULT);

  if (!(curl = curl_easy_init()))
    herror(curl, "error initializing curl", "");

  curl_easy_setopt(curl, CURLOPT_URL, "https://api.ipify.org/?format=json");
  if ((res = curl_easy_perform(curl)) != CURLE_OK)
    herror(curl, "error performing request: %s", curl_easy_strerror(res));

  curl_global_cleanup();
  exit(0);
}

void herror(CURL *curl, const char *tmpl, const char* err) {
  fprintf(stderr, tmpl, err);
  if (curl) curl_easy_cleanup(curl);
  curl_global_cleanup();
  exit(1);
}
