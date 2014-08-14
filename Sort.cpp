/**
 * @author 345570600@qq.com
 * @copyright lihao
 * @brief [七大排序算法，代码实现]
 * @details 
 * 从时间上可以看出，MAX越小，采用简单排序合适，MAX越大，采用改进的排序方法合适
 * ***********************************************************************
 * *  排序方法 *     平均情况    *  最好情况 *  最坏情况  *   辅助空间  * 稳定性 *                               
 * ***********************************************************************
 * *  冒泡排序 *     O(n^2)    *   O(n)   *  O(n^2)  *    O(1)    *  稳定  *  
 * *  选择排序 *     O(n^2)    *  O(n^2)  *  O(n^2)  *    O(1)    *  稳定  *     
 * *  插入排序 *     O(n^2)    *   O(n)   *  O(n^2)  *    O(1)    *  稳定  *  
 * *  希尔排序 *O(nlogn)~O(n^2)* O(n^1.3) *  O(n^2)  *    O(1)    * 不稳定 *  
 * *    堆排序 *    O(nlogn)   * O(nlogn) * O(nlogn) *    O(1)    * 不稳定 *  
 * *  归并排序 *    O(nlogn)   * O(nlogn) * O(nlogn) *    O(n)    *  稳定 *  
 * *  快速排序 *    O(nlogn)   * O(nlogn) *  O(n^2)  *O(logn)~O(n)* 不稳定 *  
 * ***********************************************************************
 */
#include <iostream>
#include <assert.h>
#include <time.h>
#include <boost/date_time/posix_time/posix_time.hpp>
#define MAX 100000
using namespace std;

void quick_sort(int *a,int low,int high)
{
	if(low<high)
	{
		int i=low,j=high,key=a[low];
		while(i<j)
		{
			while(i<j && a[j]>=key)
				--j;
			if(i<j)
				a[i++]=a[j];
			while(i<j && a[i]<key)
				++i;
			if(i<j)
				a[j--]=a[i];
		}
		a[i]=key;
		quick_sort(a,low,i-1);
		quick_sort(a,i+1,high);
	}	
}

void bubble_sort(int *a,int n)
{
	for(int i=0;i<n-1;i++)
	{
		for(int j=n-2;j>=i;j--)
		{
			if(a[j]>a[j+1])
			{
				a[j]=a[j]^a[j+1];
				a[j+1]=a[j]^a[j+1];
				a[j]=a[j]^a[j+1];
			}
		}
	}
}

void bubble_sort2(int *a,int n)
{
	bool flag = true;
	for(int i=0;i<n-1 && flag;i++)
	{
		flag = false;
		for(int j=n-2;j>=i;j--)
		{
			if(a[j]>a[j+1])
			{
				a[j]=a[j]^a[j+1];
				a[j+1]=a[j]^a[j+1];
				a[j]=a[j]^a[j+1];
				flag = true;
			}
		}
	}
}

void selset_sort(int *a,int n)
{
	int i,j,min;
	for(i=0;i<n-1;i++)
	{
		min=i;
		for(j=i+1;j<n;j++)
		{
			if(a[j]<a[min])
				min=j;
		}
		if(min!=i)
		{
			a[i]=a[i]^a[min];
			a[min]=a[i]^a[min];
			a[i]=a[i]^a[min];
		}
	}
}

void insert_sort(int *a,int n)
{
	int i,j,temp;
	for(i=1;i<n;i++)
	{
		if(a[i]<a[i-1])
		{
			temp=a[i];
			for(j=i-1;a[j]>temp;j--)
				a[j+1]=a[j];
			a[j+1]=temp;
		}
	}
}

void shell_sort(int *a,int n)
{
	int i,j,temp;
	int k=n;
	do
	{
		k=k/3+1;
		for(i=k;i<n;i++)
		{
			if(a[i]<a[i-k])
			{
				temp = a[i];
				for(j=i-k;j>=0 && a[j]>temp;j-=k)
					a[j+k]=a[j];
				a[j+k]=temp;
			}
		}
	}while(k>1);
}

void heapadjust(int *a,int s,int m)
{
	int i,temp=a[s];
	for(i=2*s;i<=m;i*=2)
	{
		if(i<m && a[i]<a[i+1])
			++i;
		if(temp>=a[i])
			break;
		a[s]=a[i];
		s=i;
	}
	a[s]=temp;
}
void heap_sort(int *a,int n)
{
	int i;
	for(i=n/2-1;i>=0;i--)
		heapadjust(a,i,n);
	for(i=n-1;i>0;i--)
	{
		a[0]=a[0]^a[i];
		a[i]=a[0]^a[i];
		a[0]=a[0]^a[i];
		heapadjust(a,0,i-1);
	}
}

void merge_arry(int *a,int first,int mid,int last,int *temp)
{
	int i=first,j=mid,m=mid+1,n=last;
	int k=0;
	while(i<=j && m<=n)
	{
		if(a[i]<a[m])
			temp[k++]=a[i++];
		else
			temp[k++]=a[m++];
	}
	while(i<=j)
		temp[k++]=a[i++];
	while(m<=n)
		temp[k++]=a[m++];
	for(i=0;i<k;i++)
		a[first+i]=temp[i];
}
void msort(int *a,int first,int last,int *temp)
{
	if(first<last)
	{
		int mid=(first+last)/2;
		msort(a,first,mid,temp);
		msort(a,mid+1,last,temp);
		merge_arry(a,first,mid,last,temp);
	}
}
void merge_sort(int *a,int n)
{
	int *p = new int[n];
	msort(a,0,n-1,p);
	delete[] p;
}

bool Is_increase(int *a,int n)
{
	for(int i=0;i<n-1;i++)
		if(a[i]>a[i+1])
			return false;	
	return true;		
}

int main()
{
	namespace pt=boost::posix_time;
	int a[MAX];
	srand(time(0));
	for(int i=0;i<MAX;i++)
		a[i]=rand()%MAX;

	pt::ptime quick_time_now = pt::microsec_clock::universal_time();
	quick_sort(a,0,MAX-1);
	// bubble_sort(a,MAX);
	// bubble_sort2(a,MAX);
	// selset_sort(a,MAX);
	// insert_sort(a,MAX);
	// shell_sort(a,MAX);
	// heap_sort(a,MAX);
	// merge_sort(a,MAX);
	pt::ptime quick_time_end = pt::microsec_clock::universal_time();
	pt::time_duration quick_time = quick_time_end - quick_time_now;
	assert(Is_increase(a,MAX));
	cout<<"quick_sort的运行时间为"<<quick_time<<"秒！"<<endl;
}