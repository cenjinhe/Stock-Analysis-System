const Layout = () => import('@/layout/index.vue')
const user = () => import('@/views/user/index.vue')

export default [
  {
    path: '/user-manage',
    component: Layout,
    name: 'UserManage',
    meta: {
      title: '用户管理',
    },
    icon: 'UserFilled',
    // alwaysShow: true,
    children: [
      {
        path: '',
        name: 'User',
        component: user,
        meta: {
          title: '用户列表',
        },
      },
    ],
  },
]
