/**
 * @author 345570600@qq.com
 * @copyright NULL
 * @brief [二叉排序树操作，代码实现]
 * @details 
 * 二叉排序树操作，包括二叉排序树的查找、插入、删除、整树删除，三种遍历方式
 * 
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct BiTNode
{
	int value;
	struct BiTNode *lchild,*rchild;
}*BiTree;

bool Less_than(int a,int b)  
{
	if(a<b)
		return true;
	else
		return false;
}
/*
在根指针T所指向的二叉排序树中递归地查找其关键字等于data的数据元素，若查找成功，则指针p指向该数据元素结点，并返回true，
否则指针p指向查找路径上访问的最后一个结点并返回false指针，指针f指向T的双亲，其初始调用值NULL
*/
bool SearchBST(BiTree T,int data,BiTree f,BiTree &p)
{
	if(!T)
	{
		p=f;
		return false;
	}
	else if(data==T->value)
	{
		p=T;
		return true;
	}
	else if(data<T->value)
		return SearchBST(T->lchild,data,T,p);/*左子树查找*/
	else if(data>T->value)
		return SearchBST(T->rchild,data,T,p);/*右子树查找*/
}

//当二叉排序树T中不存在关键字等于data的数据元素时，插入data
inline void InsertBST(BiTree &T,int data)     //T为传引用指针
{  
	BiTree p,s;
	if(!SearchBST(T,data,NULL,p))    //查找不成功
	{
		s=(struct BiTNode *)malloc(sizeof(BiTNode));
		s->value=data;
		s->lchild=s->rchild=NULL;
		if(p==NULL)    //二叉排序树为空的时候，被插入结点*s为新的根结点
			T=s;
		else if(Less_than(data,p->value))           //被插结点*s为左孩子
			p->lchild=s;
		else           //被插结点*s为右孩子
			p->rchild=s;
	}
	return ;
}
void PreOrderTraverse(BiTree T)    //先序遍历
{
	if(T)
	{
		printf("%d ",T->value);
		PreOrderTraverse(T->lchild);
		PreOrderTraverse(T->rchild);
	}
}
void InOrderTraverse(BiTree T)    //中序遍历
{
	if(T)
	{
		InOrderTraverse(T->lchild);
		printf("%d ",T->value);
		InOrderTraverse(T->rchild);
	}
}
void PostOrderTraverse(BiTree T)    //后序遍历
{
	if(T)
	{
		PostOrderTraverse(T->lchild);
		PostOrderTraverse(T->rchild);
		printf("%d ",T->value);
	}
}
void DeleteBSTotal(BiTree T)
{
	if(T)
	{
		DeleteBSTotal(T->lchild);    //释放左子树
		DeleteBSTotal(T->rchild);    //释放右子树
		free(T);        //释放根结点
	}
}

//从二叉排序树中删除结点p，并重接它的左或右子树。
void Delete(BiTree &p)
{

	BiTree q,s;
	if(!p->rchild) //右子树空则只需重接它的左子树（待删结点是叶子也走此分支）
	{
		q=p;
		p=p->lchild;
		free(q);
	}   
	else if(!p->lchild) //只需重接它的右子树 
	{
		q=p;
		p=p->rchild;
		free(q);
	}
	else //左右子树均不空
	{
		q=p;
		s=p->lchild;
		while(s->rchild) //转左，然后向右到尽头（找待删结点的前驱），也可以转右找后继 
		{
			q=s;
			s=s->rchild;
		}
		p->value=s->value;  //s指向被删结点的前驱（将被删结点前驱的值取代被删结点的值）
		if(q!=p)
			q->rchild=s->lchild; //重接*q的右子树 
		else
			q->lchild=s->lchild; //重接*q的左子树 
		free(s);
	}
}
//二叉排序树中删除某个结点
void DeleteBST(BiTree &T,int key)
{
	if(!T)   
		return;
	else
	{
		if(key==T->value) 
			return Delete(T);
		else if(key<T->value)
			return DeleteBST(T->lchild,key);
		else
			return DeleteBST(T->rchild,key);
	}
}

int main(void)
{
	int a[10]={62,88,58,47,35,73,51,99,37,93};
	BiTree T;
	T=NULL;
	for(int i=0;i<10;i++)
		InsertBST(T,a[i]);
	DeleteBST(T,88);
	PreOrderTraverse(T);
	printf("\n");
	InOrderTraverse(T);
	printf("\n");
	PostOrderTraverse(T);
	printf("\n");
	DeleteBSTotal(T);
	return 0;
}