<template>
  <div>
    <el-button
      style="margin: 10px 0"
      type="primary"
      @click="onCreate"
      size="mini"
      >新增</el-button
    >
    <el-table :data="tableData" stripe style="width: 100%; height: 250px">
      <el-table-column label="编号" prop="id"></el-table-column>
      <el-table-column label="姓名" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>姓名: {{ scope.row.name }}</p>
            <p>住址: {{ scope.row.address }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.name }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="性别" prop="sex"></el-table-column>
      <el-table-column label="生日" prop="bir"></el-table-column>
      <el-table-column label="地址" prop="address"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-row type="flex" justify="center">
      <el-col :span="6">
        <el-pagination
          style="margin: 15px 0"
          layout="prev, pager, next, jumper, total, sizes"
          background
          :page-size="this.pageSize"
          :page-sizes="[2, 4, 6, 8, 10]"
          :total="this.total"
          @current-change="findPage"
          @size-change="findSize"
        >
        </el-pagination
      ></el-col>
    </el-row>
    <el-dialog :title="this.dlgTitle" :visible.sync="isShow">
      <el-collapse-transition>
        <div v-show="isShow">
          <div class="transition-box">
            <el-form
              ref="userForm"
              :model="form"
              :rules="rules"
              label-width="80px"
            >
              <el-form-item label="姓名" prop="name">
                <el-input v-model="form.name"></el-input>
              </el-form-item>
              <el-form-item label="生日" prop="bir">
                <el-date-picker
                  type="date"
                  placeholder="选择日期"
                  v-model="form.bir"
                  style="width: 100%"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="性别">
                <el-radio-group v-model="form.sex">
                  <el-radio label="男"></el-radio>
                  <el-radio label="女"></el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="地址" prop="address">
                <el-input type="textarea" v-model="form.address"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit('userForm')"
                  >保存</el-button
                >
                <el-button @click="onCancel">取消</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-collapse-transition>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 4,
      isShow: false,
      dlgTitle: "用户",
      form: {
        name: "",
        bir: "",
        sex: "男",
        address: "",
      },
      rules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        bir: [{ required: true, message: "请选择出生日期", trigger: "blur" }],
        address: [{ required: true, message: "请输入地址", trigger: "blur" }],
      },
    };
  },
  methods: {
    handleEdit(index, row) {
      this.isShow = true;
      let eidtForm = Object.assign({}, row);
      console.log(index, eidtForm);
      this.form = eidtForm;
      this.dlgTitle = "编辑用户";
    },
    handleDelete(index, row) {
      console.log(index, row);
      this.$confirm("此操作将永久删除该条数据, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.axios
            .post("http://127.0.0.1:5000/delete", { id: row.id })
            .then((res) => {
              var data = res.data;
              if (data.status == true) {
                this.$message.success(data.msg);
                this.showTableData();
              } else {
                this.$message.error(data.msg);
              }
            })
            .catch((error) => {
              console.log(error);
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    showTableData(pageNum, pageSize) {
      pageNum = pageNum ? pageNum : this.pageNum;
      pageSize = pageSize ? pageSize : this.pageSize;
      this.axios
        .get(
          "http://127.0.0.1:5000/findByPage?pageNum=" +
            pageNum +
            "&pageSize=" +
            pageSize
        )
        .then((res) => {
          this.tableData = res.data.data;
          this.total = res.data.total;
        });
    },
    onCreate() {
      this.isShow = !this.isShow;
      this.form = { sex: "男" };
      this.dlgTitle = "新增用户";
    },
    onSubmit(userForm) {
      this.$refs[userForm].validate((valid) => {
        if (valid) {
          this.axios
            .post("http://127.0.0.1:5000/saveOrUpdate", this.form)
            .then((res) => {
              var data = res.data;
              if (data.status == true) {
                this.$message.success(data.msg);
                this.showTableData();
                this.form = { sex: "男" };
                this.isShow = false;
              } else {
                this.$message.error(data.msg);
              }
            })
            .catch((error) => {
              console.log(error);
            });
        } else {
          this.$message.error("当前输入的数据不合法！！");
          return false;
        }
      });
    },
    onCancel() {
      this.form = { sex: "男" };
      this.isShow = false;
    },
    findPage(page) {
      console.log(page);
      this.pageNum = page;
      this.showTableData(this.pageNum, this.pageSize);
    },
    findSize(size) {
      console.log(size);
      this.pageSize = size;
      this.showTableData(this.pageNum, this.pageSize);
    },
  },
  created() {
    this.showTableData();
  },
};
</script>

<style>
.transition-box {
  margin-bottom: 10px;
  width: 100%;
  height: 500px;
  border-radius: 4px;
  padding: 40px 20px;
  box-sizing: border-box;
  margin-right: 20px;
}
</style>