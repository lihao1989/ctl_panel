/**
 * @author 345570600@qq.com
 * @copyright NULL
 * @brief [单链表操作，代码实现]
 * @details
 * 包括单链表的插入与删除，单链表的整表创建，整表删除，单链表的读取
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
typedef struct Node
{
	int data;
	struct Node *next;
} *LinkList;

//在顺序链表L中第i个结点位置之前插入数据元素e
bool ListInsert(LinkList &L,int i, int e)
{
	int j;
	LinkList p,s;
	p = L;
	j=1;
	while(p && j<i)
	{
		p=p->next;
		++j;
	}
	if(!p || j>i)
		return false;
	s = (LinkList)malloc(sizeof(Node));
	s->data = e;
	s->next = p->next;
	p->next = s;
	return true;
}

//删除L的第i个结点，并用e返回其值
bool ListDelete(LinkList &L,int i, int *e)
{
	int j;
	LinkList p,q;
	p = L;
	j = 1;
	while( p->next && j<i)
	{
		p = p->next;
		++j;
	}
	if(!(p->next) || j>i)
		return false;
	q = p->next;
	p->next = q->next;
	*e = q->data;
	free(q);
	return true;
}

//单链表整表创建,建立带表头结点的单链线性表L(头插法，新产生的结点插入头结点后)
void CreateListHead(LinkList &L,int n)
{
	LinkList p;
	srand(time(0));
	L = (LinkList)malloc(sizeof(Node));
	L->next = NULL;
	for(int i=0;i<n;i++)
	{
		p=(LinkList)malloc(sizeof(Node));
		p->data = rand()%100+1;
		if(i==9)
			p->data = 20000;
		p->next = L->next;
		L->next = p;
	}
}

//单链表的整表删除
bool ClearList(LinkList &L)
{
	LinkList p,q;
	p = L->next; //p指向地一个结点
	while(p)
	{
		q = p->next;
		free(p);
		p=q;
	}
	L->next = NULL;
	return true;
}

//单链表的读取
bool GetElem(LinkList &L,int i,int *e)
{
	LinkList p;
	p=L->next;
	int j=0;
	while(p && j<i)
	{
		p=p->next;
		++j;
	}
	if(!p || j>i)
		return false;
	*e=p->data;
	return true;
}

int main()
{
	LinkList L;
	CreateListHead(L,10);
	int a[10],*temp;
	ListInsert(L,8,10000);
	ListDelete(L,1,&a[1]);
	printf("%d\n", a[1]);
	for (int i = 0; i < 10; ++i)
	{
		assert(GetElem(L,i,&a[i]));
		printf("%d ", a[i]);
	}
	printf("\n");
	if(ClearList(L))
		printf("单链表整表已删除!\n");
}