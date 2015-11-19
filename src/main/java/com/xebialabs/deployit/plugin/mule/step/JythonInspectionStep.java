/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
package com.xebialabs.deployit.plugin.mule.step;


import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Writer;
import java.util.Arrays;
import java.util.Map;

import javax.script.ScriptContext;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.SimpleScriptContext;

import com.xebialabs.deployit.plugin.api.flow.ExecutionContext;
import com.xebialabs.deployit.plugin.api.flow.Step;
import com.xebialabs.deployit.plugin.api.flow.StepExitCode;

public class JythonInspectionStep implements Step {

    private String inspectionScript;
    private Map<String, Object> scriptParams;
    private String description;

    public JythonInspectionStep(String inspectionScript, Map<String, Object> scriptParams, String description) {
        this.inspectionScript = inspectionScript;
        this.scriptParams = scriptParams;
        this.description = description;
    }

    @Override
    public int getOrder() {
        return 0;
    }

    @Override
    public String getDescription() {
        return description;
    }

    @Override
    public StepExitCode execute(final ExecutionContext ctx) throws Exception {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new IllegalStateException("Could not find the python/jython, is it on the classpath?");
        }
        InputStream resourceAsStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(inspectionScript);
        if (resourceAsStream == null) {
            throw new IllegalStateException("Inspection script " + inspectionScript + " not found");
        }

        engine.eval(new InputStreamReader(resourceAsStream), createScriptContext(ctx));
        return StepExitCode.SUCCESS;
    }

    private ScriptContext createScriptContext(ExecutionContext ctx) {
        SimpleScriptContext scriptContext = new SimpleScriptContext();
        scriptContext.setAttribute("inspectionContext", ctx.getInspectionContext(), ScriptContext.ENGINE_SCOPE);
        for (Map.Entry<String, Object> entry : scriptParams.entrySet()) {
            scriptContext.setAttribute(entry.getKey(), entry.getValue(), ScriptContext.ENGINE_SCOPE);
        }
        scriptContext.setWriter(new ConsumerWriter(ctx, false));
        scriptContext.setErrorWriter(new ConsumerWriter(ctx, true));
        return scriptContext;
    }

    private static class ConsumerWriter extends Writer {

        private ExecutionContext ctx;
        private boolean logToError;

        ConsumerWriter(ExecutionContext ctx, boolean logToError) {
            this.ctx = ctx;
            this.logToError = logToError;
        }

        @Override
        public void write(final char[] cbuf, final int off, final int len) throws IOException {
            char[] chars = Arrays.copyOfRange(cbuf, off, off + len);
            if (logToError) {
                ctx.logError(String.valueOf(chars));
            } else {
                ctx.logOutput(String.valueOf(chars));
            }

        }

        @Override
        public void flush() throws IOException {

        }

        @Override
        public void close() throws IOException {

        }
    }
}
