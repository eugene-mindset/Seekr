import static spark.Spark.*;

import dao.CourseDao;
import dao.DaoUtil;
import dao.InMemoryCourseDao;
import dao.InMemoryReviewDao;
import dao.ReviewDao;
import model.Course;
import model.Review;
import spark.ModelAndView;
import spark.template.handlebars.HandlebarsTemplateEngine;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;

public class WebServer {

  public static void main(String[] args) {

    // To keep things simple, we use in-memory (no persistence) DAOs
    CourseDao courseDao = new InMemoryCourseDao();
    ReviewDao reviewDao = new InMemoryReviewDao();
    DaoUtil.addSampleReviews(courseDao, reviewDao);

    get("/", (req, res) -> {
      Map<String, String> model = new HashMap<>();
      model.put("username", req.cookie("username"));
      return new ModelAndView(model, "index.hbs");
    }, new HandlebarsTemplateEngine());

    post("/", (req, res) -> {
      String username = req.queryParams("username");
      res.cookie("username", username);
      res.redirect("/");
      return null;
    });

    get("/signout", (req, res) -> {
      res.removeCookie("username");
      res.redirect("/");
      return null;
    });

    get("/courses", (req, res) -> {
      Map<String, Object> model = new HashMap<>();
      model.put("courseList", courseDao.findAll());
      return new ModelAndView(model, "courses.hbs");
    }, new HandlebarsTemplateEngine());

    post("/courses", (req, res) -> {
      String name = req.queryParams("coursename");
      String url = req.queryParams("courseurl");
      courseDao.add(new Course(name, url));
      res.redirect("/courses");
      return null;
    }, new HandlebarsTemplateEngine());

    // redirect if not logged in
    before("/courses/*",(req, res) -> {
      if (req.cookie("username") == null) {
        res.redirect("/");
      }
    });
    
    before("/courses",(req, res) -> {
      if (req.cookie("username") == null) {
        res.redirect("/");
      }
    });

    get("/courses/:course/reviews", (req, res) -> {
      Map<String, Object> model = new HashMap<>();
      model.put("reviewList", reviewDao.findByCourseId(Integer.parseInt(req.params(":course"))));
      return new ModelAndView(model, "reviews.hbs");
    }, new HandlebarsTemplateEngine());

    post("/courses/:course/reviews", (req, res) -> {
      String course = req.params(":course");
      String rating = req.queryParams("rating");
      String comment = req.queryParams("comment");
      reviewDao.add(new Review(Integer.parseInt(course), Integer.parseInt(rating), comment));
      res.redirect("/courses/" + course + "/reviews");
      return null;
    }, new HandlebarsTemplateEngine());


    // TODO add more routes to implement the expected functionalities
    //  of the web application as per homework instructions.


    // TODO you will need to have at least one more template file: reviews.hbs, and
    //  you will probably need to modify the ones provided to you.

  }
}
