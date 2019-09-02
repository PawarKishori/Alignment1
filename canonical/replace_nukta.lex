%{
#include<string.h>
char str[10000];
%}

start_tag "@"
end_tag "@"

%%

aZ printf("Za");
AZ printf("ZA");
iZ printf("Zi");
IZ printf("ZI");
uZ printf("Zu");
UZ printf("ZU");
eZ printf("Ze");
EZ printf("ZE");
oZ printf("Zo");
OZ printf("ZO");
{start_tag}[a-zA-Z#\-_0-9]{end_tag} printf("%s",yytext);
%%
