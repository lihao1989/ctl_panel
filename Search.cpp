/**
 * @author 345570600@qq.com
 * @copyright NULL
 * @brief [查找操作，代码实现]
 * @details
 * 包括有序查找中的二分查找，插值查找，非波那契查找
 * 无序查找中的顺序查找很easy，需要注意的是，在while循环遍历的时候通过设置标兵，可以减少比较的次数
 */
#include <iostream>
using namespace std;

int F[100];
//二分查找
int binary_search(int *a,int n,int key)
{
	int low=0,high=n-1,mid;
	while(low<=high)
	{
		mid = low+(high-low)/2;
		if(key<a[mid])
			high=mid-1;
		else if(key>a[mid])
			low=mid+1;
		else
			return mid;
	}
	return -1;
}

//插值查找,easy
int inter_search(int *a,int n,int key)
{
	int low=0,high=n-1,mid;
	while(low<=high)
	{
		mid = low+(high-low)*(key-a[low])/(a[high]-a[low]);
		if(key<a[mid])
			high=mid-1;
		else if(key>a[mid])
			low=mid+1;
		else
			return mid;
	}
	return -1;
}

//非波那契查找
int fibonacci_search(int *a,int n,int key)
{
	int k=0;
	int low=0,high=n-1,mid;
	while(n>F[k])
		++k;
	for(int i=n;i<=F[k];++i)
		a[i]=a[n-1];

	while(low<=high)
	{
		mid =low + F[k-1];
		if(key<a[mid])
		{
			high=mid-1;
			k=k-1;
		}
		else if(key>a[mid])
		{
			low=mid+1;
			k=k-2;
		}
		else
		{
			if(mid<n)
				return mid;
			else
				return n-1;
		}
	}
	return -1;
}

int main()  
{  
    int a[10] = {1,16,24,35,47,59,62,73,88,99};  
    F[0]=0;  
    F[1]=1;  
    for(int i = 2;i < 100;i++)    
    {   
        F[i] = F[i-1] + F[i-2];    
    }   
    cout<<binary_search(a,10,99)<<endl;//如果返回-1，则查找失败  
    cout<<inter_search(a,10,99)<<endl;//如果返回-1，则查找失败  
    cout<<fibonacci_search(a,10,99)<<endl;//如果返回-1，则查找失败  
    return 0;  
}  
