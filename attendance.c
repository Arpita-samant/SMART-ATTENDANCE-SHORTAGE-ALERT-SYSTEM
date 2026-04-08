#include<stdio.h>
#include<stdlib.h>

int main(int argc,char *argv[])
{
    FILE *file=fopen(argv[1],"r");
    FILE *output=fopen("low_attendance.csv","w");

    char roll[20],name[50],email[100];
    int attendance;

    fscanf(file,"%[^,],%[^,],%[^,],%s\n",roll,name,email,name);

    while(fscanf(file,"%[^,],%[^,],%[^,],%d\n",roll,name,email,&attendance)!=EOF)
    {
        if(attendance<75)
        {
            fprintf(output,"%s,%s,%s,%d\n",roll,name,email,attendance);
        }
    }

    fclose(file);
    fclose(output);

    return 0;
}