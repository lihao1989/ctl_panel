/**
 * @author 345570600@qq.com
 * @copyright NULL
 * @brief [字符串匹配操作，代码实现]
 * @details
 * 查找子串在主串中的位置，如果不存在返回-1
 * 包括普通匹配方法和KMP模式匹配，KMP模式匹配难点在于求next数组
 */
#include <iostream>
#include <cstring>
using namespace std;
/**
 * @brief [计算子串T的next数组]
 * 
 * @param T [子串]
 * @param n [长度]
 * @param next [数组]
 * @T[i]表示后缀单个字符，T[j]表示前缀单个字符，默认情况下next[0]=-1,j=-1
 */
void get_next(char* T,int n,int *next)
{
	int i=0,j=-1;
	next[0]=-1;
	while(i<n)
	{
		if(j==-1 ||T[i]==T[j])
		{
			++j;
			++i;
			next[i]=j;
		}
		else
			j=next[j];
	}
}

/**
 * @brief [KMP查找子串T在主串S中的位置，如果不存在返回-1]
 * 
 * @param m [主串S长度]
 * @param n [子串T长度]
 */
int index_KMP(char* S,char* T,int m,int n)
{
	int i=0;
	int j=0;
	int next[100];
	get_next(T,n,next);
	while(i<m && j<n)
	{
		if(j==-1 ||S[i]==T[j])
		{
			++i;
			++j;
		}
		else
			j=next[j];
	}
	if(j>=n)
		return i-n;
	else
		return -1;
}

/**
 * @brief [普通查找子串在主串中的位置，如果不存在返回-1]
 * 
 * @param m [主串S长度]
 * @param n [子串T长度]
 */
int index(char *S,char *T,int m,int n)
{
	int i=0,j=0;
	while(i<m &&j<n)
	{
		if(S[i]==T[j])
		{
			++i;
			++j;
		}
		else
		{
			i=i-j+1;
			j=0;
		}
	}
	if(j>=n)
		return i-n;
	else 
		return -1;
}

int main()
{
	char S[]="aaaaaaaabcdaaa";
	char T[]="abcd";
	cout<<index_KMP(S,T,strlen(S),strlen(T))<<endl;
	cout<<index(S,T,strlen(S),strlen(T))<<endl;
	return 0;
}