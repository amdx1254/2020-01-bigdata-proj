import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.ml.linalg.{Vector, Vectors}
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.expressions.UserDefinedFunction
import math.log

object cosinesimilarityUDFs {

	def consinesimilarity(vectorA: Vector, vectorB: Vector): Double = {
	  var dotProduct = 0.0
          var normA = 0.0
          var normB = 0.0
          var index = vectorA.size - 1

          for (i <- 0 to index) {
            dotProduct += vectorA(i) * vectorB(i)
            normA += Math.pow(vectorA(i), 2)
            normB += Math.pow(vectorB(i), 2)
          }
          (dotProduct / (Math.sqrt(normA) * Math.sqrt(normB)))
        }

        def cosinesimilarityUDF: UserDefinedFunction = udf((vectora: Vector, vectorb: Vector) => consinesimilarity(vectora,vectorb))
	  
  	def registerUdf: UserDefinedFunction = {
  		val spark = SparkSession.builder().getOrCreate()
  		spark.udf.register("consinesimilarity", (a: Vector, b: Vector) => consinesimilarity(a, b))
  }
}
