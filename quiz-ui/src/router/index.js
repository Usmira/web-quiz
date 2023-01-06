import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import ScorePage from '../views/ScorePage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminPage from '../views/AdminPage.vue'
import DetailPage from '../views/DetailPage.vue'
import NewQuestionPage from '../views/NewQuestionPage.vue'
import EditQuestionPage from '../views/EditQuestionPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/start-new-quiz-page",
      name: "NewQuizPage",
      component: NewQuizPage,
    },
    {
      path: "/questions",
      name: "QuestionManager",
      component: QuestionManager,
    },
    {
      path: "/your-score",
      name: "ScorePage",
      component: ScorePage,
    },
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage,
    },
    {
      path: "/admin-list-questions",
      name: "AdminPage",
      component: AdminPage,
    },
    {
      path: "/admin-detail-question",
      name: "DetailPage",
      component: DetailPage,
    },
    {
      path: "/create-new-question",
      name: "NewQuestionPage",
      component: NewQuestionPage,
    },
    {
      path: "/edit-question",
      name: "EditQuestionPage",
      component: EditQuestionPage,
    }
  ]
})

export default router
